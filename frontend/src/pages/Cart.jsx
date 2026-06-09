import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { fetchCart, removeFromCart } from '../store/slices/cartSlice'

export default function Cart() {
  const dispatch = useDispatch()
  const { items, subtotal, tax, discount, total, itemCount } = useSelector((s) => s.cart)

  useEffect(() => { dispatch(fetchCart()) }, [dispatch])

  if (itemCount === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold mb-4">Your cart is empty</h2>
        <Link to="/products" className="btn-primary">Continue Shopping</Link>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Shopping Cart ({itemCount} items)</h1>
      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          {items.map((item) => (
            <div key={item.id} className="card p-4 flex gap-4">
              {item.product?.primary_image && (
                <img src={item.product.primary_image} alt="" className="w-24 h-24 object-cover rounded-lg" />
              )}
              <div className="flex-1">
                <h3 className="font-medium">{item.product?.name}</h3>
                <p className="text-gocart-orange font-bold mt-1">₹{item.subtotal}</p>
                <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
              </div>
              <button onClick={() => dispatch(removeFromCart(item.product.id))} className="text-red-500 hover:underline text-sm">Remove</button>
            </div>
          ))}
        </div>
        <div className="card p-6 h-fit">
          <h3 className="font-bold text-lg mb-4">Order Summary</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span>Subtotal</span><span>₹{subtotal}</span></div>
            <div className="flex justify-between"><span>Tax</span><span>₹{tax}</span></div>
            {discount > 0 && <div className="flex justify-between text-green-600"><span>Discount</span><span>-₹{discount}</span></div>}
            <div className="flex justify-between font-bold text-lg border-t pt-2"><span>Total</span><span>₹{total}</span></div>
          </div>
          <Link to="/checkout" className="btn-primary w-full block text-center mt-6">Proceed to Checkout</Link>
        </div>
      </div>
    </div>
  )
}
