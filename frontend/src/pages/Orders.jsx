import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ordersAPI } from '../services/api'

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800',
  processing: 'bg-blue-100 text-blue-800',
  shipped: 'bg-purple-100 text-purple-800',
  delivered: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800',
  returned: 'bg-gray-100 text-gray-800',
}

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    ordersAPI.list().then(({ data }) => {
      setOrders(data.results || [])
      setLoading(false)
    })
  }, [])

  if (loading) return <div className="max-w-7xl mx-auto px-4 py-8 animate-pulse"><div className="h-32 bg-gray-200 dark:bg-gray-700 rounded-xl" /></div>

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">My Orders</h1>
      {orders.length === 0 ? (
        <p className="text-gray-500">No orders yet.</p>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <Link key={order.id} to={`/orders/${order.id}`} className="card p-4 flex justify-between items-center hover:shadow-md transition-shadow block">
              <div>
                <p className="font-medium">{order.order_number}</p>
                <p className="text-sm text-gray-500">{new Date(order.created_at).toLocaleDateString()} · {order.items_count} items</p>
              </div>
              <div className="text-right">
                <p className="font-bold">₹{order.total}</p>
                <span className={`text-xs px-2 py-1 rounded-full ${statusColors[order.status] || ''}`}>{order.status}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
