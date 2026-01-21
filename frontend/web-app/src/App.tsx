import { useState, useEffect } from 'react'
import axios from 'axios'

// Environment variables can be injected via config in k8s
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface User {
    id: number;
    username: string;
    email: string;
}

interface Order {
    id: number;
    item_name: string;
    quantity: number;
    price: number;
}

function App() {
    const [users, setUsers] = useState<User[]>([]);
    const [orders, setOrders] = useState<Order[]>([]);
    const [userForm, setUserForm] = useState({ username: '', email: '' });
    const [orderForm, setOrderForm] = useState({ user_id: 1, item_name: '', quantity: 1, price: 0 });

    const fetchUsers = async () => {
        try {
            const res = await axios.get(`${API_URL}/users/`);
            setUsers(res.data);
        } catch (e) { console.error(e) }
    };

    const fetchOrders = async () => {
        try {
            const res = await axios.get(`${API_URL}/orders/`);
            setOrders(res.data);
        } catch (e) { console.error(e) }
    };

    useEffect(() => {
        fetchUsers();
        fetchOrders();
    }, [])

    const handleUserSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post(`${API_URL}/users/`, userForm);
            fetchUsers();
        } catch (e) { alert('Error creating user') }
    };

    const handleOrderSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post(`${API_URL}/orders/`, orderForm);
            fetchOrders();
        } catch (e) { alert('Error creating order') }
    };

    return (
        <div style={{ padding: '2rem' }}>
            <h1>Antigravity K8s Lab</h1>

            <div style={{ display: 'flex', gap: '2rem' }}>
                <div>
                    <h2>Users</h2>
                    <form onSubmit={handleUserSubmit}>
                        <input placeholder="Username" value={userForm.username} onChange={e => setUserForm({ ...userForm, username: e.target.value })} />
                        <input placeholder="Email" value={userForm.email} onChange={e => setUserForm({ ...userForm, email: e.target.value })} />
                        <button type="submit">Create User</button>
                    </form>
                    <ul>
                        {users.map(u => <li key={u.id}>{u.username} ({u.email})</li>)}
                    </ul>
                </div>

                <div>
                    <h2>Orders</h2>
                    <form onSubmit={handleOrderSubmit}>
                        <input placeholder="Item" value={orderForm.item_name} onChange={e => setOrderForm({ ...orderForm, item_name: e.target.value })} />
                        <input type="number" placeholder="Qty" value={orderForm.quantity} onChange={e => setOrderForm({ ...orderForm, quantity: Number(e.target.value) })} />
                        <input type="number" placeholder="Price" value={orderForm.price} onChange={e => setOrderForm({ ...orderForm, price: Number(e.target.value) })} />
                        <button type="submit">Create Order</button>
                    </form>
                    <ul>
                        {orders.map(o => <li key={o.id}>{o.item_name} - ${o.price}</li>)}
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default App
