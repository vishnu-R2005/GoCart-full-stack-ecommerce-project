import { lazy, Suspense, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import Layout from './components/layout/Layout'
import ErrorBoundary from './components/common/ErrorBoundary'
import ProtectedRoute from './components/auth/ProtectedRoute'
import { ProductGridSkeleton } from './components/common/Skeleton'
import { setDarkMode } from './store/slices/themeSlice'
import { fetchCart } from './store/slices/cartSlice'

const Home = lazy(() => import('./pages/Home'))
const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))
const ForgotPassword = lazy(() => import('./pages/ForgotPassword'))
const ResetPassword = lazy(() => import('./pages/ResetPassword'))
const Products = lazy(() => import('./pages/Products'))
const ProductDetail = lazy(() => import('./pages/ProductDetail'))
const Cart = lazy(() => import('./pages/Cart'))
const Checkout = lazy(() => import('./pages/Checkout'))
const Wishlist = lazy(() => import('./pages/Wishlist'))
const Orders = lazy(() => import('./pages/Orders'))
const OrderDetail = lazy(() => import('./pages/OrderDetail'))
const Profile = lazy(() => import('./pages/Profile'))
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'))

function PageLoader() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <ProductGridSkeleton />
    </div>
  )
}

export default function App() {
  const dispatch = useDispatch()
  const { darkMode } = useSelector((s) => s.theme)
  const { isAuthenticated } = useSelector((s) => s.auth)
  const AdminProducts = lazy(() => import('./pages/admin/AdminProducts'))
  const AddProduct = lazy(() => import('./pages/admin/AddProduct'))

  useEffect(() => {
    dispatch(setDarkMode(darkMode))
  }, [])

  useEffect(() => {
    if (isAuthenticated) dispatch(fetchCart())
  }, [isAuthenticated, dispatch])

  return (
    <ErrorBoundary>
      <Layout>
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/products" element={<Products />} />
            <Route path="/products/:slug" element={<ProductDetail />} />
            <Route path="/cart" element={<ProtectedRoute><Cart /></ProtectedRoute>} />
            <Route path="/checkout" element={<ProtectedRoute><Checkout /></ProtectedRoute>} />
            <Route path="/wishlist" element={<ProtectedRoute><Wishlist /></ProtectedRoute>} />
            <Route path="/orders" element={<ProtectedRoute><Orders /></ProtectedRoute>} />
            <Route path="/orders/:id" element={<ProtectedRoute><OrderDetail /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
            <Route path="/admin" element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>} />
            <Route path="/admin/products" element={<ProtectedRoute adminOnly><AdminProducts /></ProtectedRoute>}/>
            <Route path="/admin/products/add" element={<ProtectedRoute adminOnly><AddProducts /></ProtectedRoute>}/>
          </Routes>
        </Suspense>
      </Layout>
    </ErrorBoundary>
  )
}
