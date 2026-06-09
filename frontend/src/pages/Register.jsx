import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import toast from 'react-hot-toast'
import { registerUser } from '../store/slices/authSlice'

export default function Register() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm()
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const onSubmit = async (data) => {
    try {
      await dispatch(registerUser(data)).unwrap()
      toast.success('Account created! Please verify your email.')
      navigate('/')
    } catch (err) {
      const msg = err?.email?.[0] || err?.password_confirm?.[0] || 'Registration failed'
      toast.error(msg)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="card p-8">
        <h2 className="text-2xl font-bold text-center mb-6">Create GoCart Account</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <input {...register('first_name')} placeholder="First Name" className="input-field" />
            </div>
            <div>
              <input {...register('last_name')} placeholder="Last Name" className="input-field" />
            </div>
          </div>
          <input {...register('email', { required: 'Email required' })} type="email" placeholder="Email" className="input-field" />
          {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}
          <input {...register('phone')} placeholder="Phone (optional)" className="input-field" />
          <input {...register('password', { required: 'Password required', minLength: 8 })} type="password" placeholder="Password" className="input-field" />
          <input
            {...register('password_confirm', { required: true, validate: (v) => v === watch('password') || 'Passwords must match' })}
            type="password" placeholder="Confirm Password" className="input-field"
          />
          {errors.password_confirm && <p className="text-red-500 text-sm">{errors.password_confirm.message}</p>}
          <button type="submit" className="btn-primary w-full">Create Account</button>
        </form>
        <p className="text-center mt-4 text-sm">
          Already have an account? <Link to="/login" className="text-gocart-orange hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  )
}
