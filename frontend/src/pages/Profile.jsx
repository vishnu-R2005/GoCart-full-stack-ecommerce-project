import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useDispatch, useSelector } from 'react-redux'
import toast from 'react-hot-toast'
import { authAPI, addressesAPI } from '../services/api'
import { fetchProfile } from '../store/slices/authSlice'

export default function Profile() {
  const dispatch = useDispatch()
  const { user } = useSelector((s) => s.auth)
  const [addresses, setAddresses] = useState([])
  const { register, handleSubmit, reset } = useForm()

  useEffect(() => {
    dispatch(fetchProfile())
    addressesAPI.list().then(({ data }) => setAddresses(data.results || []))
  }, [dispatch])

  useEffect(() => {
    if (user) reset({ first_name: user.first_name, last_name: user.last_name, phone: user.phone })
  }, [user, reset])

  const onUpdate = async (data) => {
    try {
      await authAPI.updateProfile(data)
      dispatch(fetchProfile())
      toast.success('Profile updated')
    } catch {
      toast.error('Update failed')
    }
  }

  const onAddAddress = async (e) => {
    e.preventDefault()
    const form = new FormData(e.target)
    const data = Object.fromEntries(form)
    try {
      await addressesAPI.create(data)
      const { data: res } = await addressesAPI.list()
      setAddresses(res.results || [])
      e.target.reset()
      toast.success('Address added')
    } catch {
      toast.error('Failed to add address')
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
      <div className="card p-6">
        <h2 className="text-xl font-bold mb-4">Profile</h2>
        <form onSubmit={handleSubmit(onUpdate)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <input {...register('first_name')} placeholder="First Name" className="input-field" />
            <input {...register('last_name')} placeholder="Last Name" className="input-field" />
          </div>
          <input {...register('phone')} placeholder="Phone" className="input-field" />
          <p className="text-sm text-gray-500">Email: {user?.email}</p>
          <button type="submit" className="btn-primary">Save Changes</button>
        </form>
      </div>

      <div className="card p-6">
        <h2 className="text-xl font-bold mb-4">Addresses</h2>
        {addresses.map((a) => (
          <div key={a.id} className="border-b py-3 text-sm">
            <p className="font-medium">{a.full_name}</p>
            <p className="text-gray-500">{a.address_line1}, {a.city}, {a.state} {a.postal_code}</p>
          </div>
        ))}
        <form onSubmit={onAddAddress} className="mt-4 space-y-3">
          <input name="full_name" required placeholder="Full Name" className="input-field" />
          <input name="phone" required placeholder="Phone" className="input-field" />
          <input name="address_line1" required placeholder="Address" className="input-field" />
          <div className="grid grid-cols-2 gap-3">
            <input name="city" required placeholder="City" className="input-field" />
            <input name="state" required placeholder="State" className="input-field" />
          </div>
          <input name="postal_code" required placeholder="Postal Code" className="input-field" />
          <button type="submit" className="btn-secondary">Add Address</button>
        </form>
      </div>
    </div>
  )
}
