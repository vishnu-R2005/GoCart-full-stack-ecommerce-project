import { useForm } from 'react-hook-form'
import { Link, useSearchParams, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { authAPI } from '../services/api'

export default function ResetPassword() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const token = params.get('token')
  const { register, handleSubmit, watch } = useForm()

  const onSubmit = async (data) => {
    try {
      await authAPI.resetPassword({ token, new_password: data.password, new_password_confirm: data.password_confirm })
      toast.success('Password reset successfully!')
      navigate('/login')
    } catch {
      toast.error('Invalid or expired reset link')
    }
  }

  if (!token) {
    return (
      <div className="text-center py-12">
        <p>Invalid reset link.</p>
        <Link to="/forgot-password" className="text-gocart-orange">Request new link</Link>
      </div>
    )
  }

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="card p-8">
        <h2 className="text-2xl font-bold text-center mb-6">Reset Password</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <input {...register('password', { required: true, minLength: 8 })} type="password" placeholder="New Password" className="input-field" />
          <input
            {...register('password_confirm', { validate: (v) => v === watch('password') })}
            type="password" placeholder="Confirm Password" className="input-field"
          />
          <button type="submit" className="btn-primary w-full">Reset Password</button>
        </form>
      </div>
    </div>
  )
}
