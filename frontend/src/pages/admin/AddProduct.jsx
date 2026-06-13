import { useEffect,useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { productsAPI } from '../../services/api'

export default function AddProducts() {
  const navigate = useNavigate()

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    discount_price: '',
    stock: '',
    sku: '',
    brand: '',
    category: '',
    is_featured: false,
    is_active: true,
  })

  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target

    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      setLoading(true)

      await productsAPI.create({
        ...formData,
        price: Number(formData.price),
        discount_price: formData.discount_price
          ? Number(formData.discount_price)
          : null,
        stock: Number(formData.stock),
        category: Number(formData.category),
      })

      toast.success('Product created successfully')

      navigate('/admin/products')
    } catch (error) {
      console.error(error)
      toast.error('Failed to create product')
    } finally {
      setLoading(false)
    }
  }

  const [categories, setCategories] = useState([])

  useEffect(() => {
  const loadCategories = async () => {
    try {
      const { data } = await productsAPI.categories()

      setCategories(data.results || data)
    } catch (error) {
      console.error(error)
      toast.error('Failed to load categories')
    }
  }

  loadCategories()
}, [])


  return (
    <div className="max-w-4xl mx-auto px-4 py-8">

      <h1 className="text-2xl font-bold mb-6">
        Add Product
      </h1>

      <form
        onSubmit={handleSubmit}
        className="card p-6 space-y-4"
      >

        <input
          name="name"
          placeholder="Product Name"
          className="input-field"
          onChange={handleChange}
          required
        />

        <textarea
          name="description"
          placeholder="Description"
          className="input-field"
          rows="4"
          onChange={handleChange}
        />

        <div className="grid md:grid-cols-2 gap-4">

          <input
            name="price"
            type="number"
            placeholder="Price"
            className="input-field"
            onChange={handleChange}
            required
          />

          <input
            name="discount_price"
            type="number"
            placeholder="Discount Price"
            className="input-field"
            onChange={handleChange}
          />

          <input
            name="stock"
            type="number"
            placeholder="Stock"
            className="input-field"
            onChange={handleChange}
            required
          />

          <input
            name="sku"
            placeholder="SKU"
            className="input-field"
            onChange={handleChange}
            required
          />

          <input
            name="brand"
            placeholder="Brand"
            className="input-field"
            onChange={handleChange}
          />

         <select
  name="category"
  value={formData.category}
  onChange={handleChange}
  className="input-field"
  required
>
    <option value="">
        Select Category
    </option>

    {categories.map((category) => (
        <option
        key={category.id}
        value={category.id}
        >
        {category.name}
        </option>
    ))}
    </select>

        </div>

        <div className="flex gap-6">

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              name="is_featured"
              onChange={handleChange}
            />
            Featured
          </label>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              name="is_active"
              checked={formData.is_active}
              onChange={handleChange}
            />
            Active
          </label>

        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn-primary"
        >
          {loading ? 'Creating...' : 'Create Product'}
        </button>

      </form>
    </div>
  )
}
