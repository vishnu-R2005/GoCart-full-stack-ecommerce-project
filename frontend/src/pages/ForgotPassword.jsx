import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import { authAPI } from '../services/api'

export default function ForgotPassword() {
  const { register, handleSubmit } = useForm()

  const onSubmit = async ({ email }) => {
    try {
      await authAPI.forgotPassword(email)
      toast.success('If the email exists, a reset link has been sent.')
    } catch {
      toast.error('Something went wrong')
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="card p-8">
        <h2 className="text-2xl font-bold text-center mb-6">Forgot Password</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <input {...register('email', { required: true })} type="email" placeholder="Enter your email" className="input-field" />
          <button type="submit" className="btn-primary w-full">Send Reset Link</button>
        </form>
        <p className="text-center mt-4 text-sm">
          <Link to="/login" className="text-gocart-orange hover:underline">Back to login</Link>
        </p>
      </div>
    </div>
  )
}
