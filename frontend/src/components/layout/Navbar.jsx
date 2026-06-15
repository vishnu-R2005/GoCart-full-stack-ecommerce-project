import { Link } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { toggleDarkMode } from '../../store/slices/themeSlice'
import { logout } from '../../store/slices/authSlice'

export default function Navbar() {
  const dispatch = useDispatch()
  const { isAuthenticated, user } = useSelector((s) => s.auth)
  const { itemCount } = useSelector((s) => s.cart)
  const { darkMode } = useSelector((s) => s.theme)

  return (
    <header className="bg-gocart-dark text-white sticky top-0 z-50 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between gap-4">
          <Link to="/" className="flex-shrink-0">
            <h1 className="text-2xl font-bold text-gocart-orange">GoCart</h1>
            <p className="text-xs text-gray-400 hidden sm:block">Shop Smarter. Shop Faster.</p>
          </Link>

          <form className="flex-1 max-w-xl hidden md:block" onSubmit={(e) => e.preventDefault()}>
            <div className="flex">
              <input
                type="search"
                placeholder="Search products..."
                className="flex-1 px-4 py-2 rounded-l-lg text-gray-900 outline-none"
              />
              <button type="submit" className="bg-gocart-orange px-4 py-2 rounded-r-lg hover:bg-orange-600">
                Search
              </button>
            </div>
          </form>

          <nav className="flex items-center gap-3 sm:gap-5">
            <button
              onClick={() => dispatch(toggleDarkMode())}
              className="p-2 rounded-lg hover:bg-gray-700"
              aria-label="Toggle dark mode"
            >
              {darkMode ? '☀️' : '🌙'}
            </button>

          {isAuthenticated ? (
  user?.role === 'admin' ? (
    <>
      <Link
        to="/admin"
        className="hover:text-gocart-orange text-sm"
      >
        Admin
      </Link>

      <button
        onClick={() => dispatch(logout())}
        className="text-sm hover:text-gocart-orange"
      >
        Logout
      </button>
    </>
  ) : (
    <>
      <Link
        to="/orders"
        className="hover:text-gocart-orange text-sm hidden sm:inline"
      >
        Orders
      </Link>

      <Link
        to="/wishlist"
        className="hover:text-gocart-orange text-sm hidden sm:inline"
      >
        Wishlist
      </Link>

      <Link
        to="/profile"
        className="hover:text-gocart-orange text-sm hidden sm:inline"
      >
        Profile
      </Link>

      <Link
        to="/cart"
        className="relative hover:text-gocart-orange"
      >
        🛒

        {itemCount > 0 && (
          <span className="absolute -top-2 -right-2 bg-gocart-orange text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {itemCount}
          </span>
        )}
      </Link>

      <button
        onClick={() => dispatch(logout())}
        className="text-sm hover:text-gocart-orange"
      >
        Logout
      </button>
    </>
  )
) : (
              <>
                <Link to="/login" className="hover:text-gocart-orange text-sm">Login</Link>
                <Link to="/register" className="btn-primary text-sm py-1.5 px-3">Sign Up</Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
