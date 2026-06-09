import { useForm } from 'react-hook-form'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import toast from 'react-hot-toast'
import { loginUser } from '../store/slices/authSlice'

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm()
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const location = useLocation()
  const { loading } = useSelector((s) => s.auth)
  const from = location.state?.from?.pathname || '/'

  const onSubmit = async (data) => {
    try {
      await dispatch(loginUser(data)).unwrap()
      toast.success('Welcome back!')
      navigate(from)
    } catch (err) {
      toast.error(err?.detail || 'Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="card p-8">
        <h2 className="text-2xl font-bold text-center mb-2">Sign In to GoCart</h2>
        <p className="text-center text-gray-500 mb-6">Shop Smarter. Shop Faster.</p>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input {...register('email', { required: 'Email is required' })} type="email" className="input-field" />
            {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input {...register('password', { required: 'Password is required' })} type="password" className="input-field" />
            {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>}
          </div>
          <div className="text-right">
            <Link to="/forgot-password" className="text-sm text-gocart-orange hover:underline">Forgot password?</Link>
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <p className="text-center mt-4 text-sm">
          New to GoCart? <Link to="/register" className="text-gocart-orange hover:underline">Create account</Link>
        </p>
      </div>
    </div>
  )
}
