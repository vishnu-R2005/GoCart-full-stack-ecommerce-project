import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import { ordersAPI } from '../services/api'

export default function OrderDetail() {
  const { id } = useParams()
  const [order, setOrder] = useState(null)

  useEffect(() => {
    ordersAPI.get(id).then(({ data }) => setOrder(data.order || data))
  }, [id])

  const handleCancel = async () => {
    try {
      const { data } = await ordersAPI.cancel(id)
      setOrder(data.order)
      toast.success('Order cancelled')
    } catch {
      toast.error('Cannot cancel this order')
    }
  }

  if (!order) return <div className="max-w-7xl mx-auto px-4 py-8 animate-pulse"><div className="h-64 bg-gray-200 rounded-xl" /></div>

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link to="/orders" className="text-gocart-orange text-sm mb-4 inline-block">← Back to Orders</Link>
      <div className="card p-6">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-2xl font-bold">{order.order_number}</h1>
            <p className="text-gray-500">{new Date(order.created_at).toLocaleString()}</p>
          </div>
          <span className="px-3 py-1 rounded-full bg-gray-100 text-sm capitalize">{order.status}</span>
        </div>

        <div className="space-y-3 mb-6">
          {order.items?.map((item) => (
            <div key={item.id} className="flex justify-between border-b pb-2">
              <span>{item.product_name} x{item.quantity}</span>
              <span>₹{item.total_price}</span>
            </div>
          ))}
        </div>

        <div className="border-t pt-4 space-y-1 text-sm">
          <div className="flex justify-between"><span>Subtotal</span><span>₹{order.subtotal}</span></div>
          <div className="flex justify-between"><span>Tax</span><span>₹{order.tax}</span></div>
          {order.discount > 0 && <div className="flex justify-between text-green-600"><span>Discount</span><span>-₹{order.discount}</span></div>}
          <div className="flex justify-between font-bold text-lg"><span>Total</span><span>₹{order.total}</span></div>
        </div>

        {order.tracking_number && (
          <p className="mt-4 text-sm">Tracking: <strong>{order.tracking_number}</strong></p>
        )}

        {['pending', 'processing'].includes(order.status) && (
          <button onClick={handleCancel} className="mt-6 text-red-500 hover:underline text-sm">Cancel Order</button>
        )}
      </div>
    </div>
  )
}
