import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useSelector } from 'react-redux'
import toast from 'react-hot-toast'
import { addressesAPI, ordersAPI, paymentsAPI } from '../services/api'

export default function Checkout() {
  const navigate = useNavigate()
  const { total } = useSelector((s) => s.cart)
  const [addresses, setAddresses] = useState([])
  const [coupon, setCoupon] = useState('')
  const [loading, setLoading] = useState(false)
  const { register, handleSubmit } = useForm()

  useEffect(() => {
    addressesAPI.list().then(({ data }) => setAddresses(data.results || []))
  }, [])

  const loadRazorpay = () => new Promise((resolve) => {
    const script = document.createElement('script')
    script.src = 'https://checkout.razorpay.com/v1/checkout.js'
    script.onload = () => resolve(true)
    script.onerror = () => resolve(false)
    document.body.appendChild(script)
  })

  const onSubmit = async (formData) => {
    setLoading(true)
    try {
      const orderData = {
        shipping_address_id: formData.shipping_address_id,
        billing_address_id: formData.billing_address_id || formData.shipping_address_id,
        coupon_code: coupon || undefined,
        notes: formData.notes,
      }
      const { data: orderRes } = await ordersAPI.place(orderData)
      const order = orderRes.order

      const loaded = await loadRazorpay()
      if (!loaded) {
        toast.success('Order placed! (Payment gateway unavailable in dev)')
        navigate(`/orders/${order.id}`)
        return
      }

     toast.success('Order placed successfully!')
navigate(`/orders/${order.id}`)
return
      const rzp = new window.Razorpay(options)
      rzp.open()
    } catch (err) {
      toast.error(err.response?.data?.error?.detail || 'Checkout failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Checkout</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="card p-6">
          <h3 className="font-bold mb-4">Shipping Address</h3>
          {addresses.length === 0 ? (
            <p className="text-gray-500">No addresses. <a href="/profile" className="text-gocart-orange">Add one in profile</a></p>
          ) : (
            <select {...register('shipping_address_id', { required: true })} className="input-field">
              {addresses.map((a) => (
                <option key={a.id} value={a.id}>{a.full_name} - {a.address_line1}, {a.city}</option>
              ))}
            </select>
          )}
        </div>

        <div className="card p-6">
          <h3 className="font-bold mb-4">Coupon Code</h3>
          <div className="flex gap-2">
            <input value={coupon} onChange={(e) => setCoupon(e.target.value)} placeholder="Enter coupon" className="input-field" />
            <button type="button" onClick={async () => {
              try {
                const { data } = await ordersAPI.applyCoupon(coupon)
                toast.success(`Discount: ₹${data.discount}`)
              } catch { toast.error('Invalid coupon') }
            }} className="btn-secondary">Apply</button>
          </div>
        </div>

        <div className="card p-6">
          <textarea {...register('notes')} placeholder="Order notes (optional)" className="input-field" rows={3} />
        </div>

        <div className="card p-6 flex justify-between items-center">
          <span className="text-xl font-bold">Total: ₹{total}</span>
          <button type="submit" disabled={loading || addresses.length === 0} className="btn-primary px-8">
            {loading ? 'Processing...' : 'Place Order & Pay'}
          </button>
        </div>
      </form>
    </div>
  )
}
