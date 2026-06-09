import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-gocart-dark text-gray-400 mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-gocart-orange text-xl font-bold mb-2">GoCart</h3>
            <p className="text-sm">Shop Smarter. Shop Faster.</p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Shop</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/products" className="hover:text-gocart-orange">All Products</Link></li>
              <li><Link to="/products?featured=true" className="hover:text-gocart-orange">Featured</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Account</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/orders" className="hover:text-gocart-orange">Orders</Link></li>
              <li><Link to="/wishlist" className="hover:text-gocart-orange">Wishlist</Link></li>
              <li><Link to="/profile" className="hover:text-gocart-orange">Profile</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Support</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="/api/docs/" className="hover:text-gocart-orange">API Docs</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-sm">
          © {new Date().getFullYear()} GoCart. All rights reserved.
        </div>
      </div>
    </footer>
  )
}
