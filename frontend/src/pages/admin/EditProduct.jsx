import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import toast from 'react-hot-toast'
import { productsAPI } from '../../services/api'

export default function EditProduct() {
  const { slug } = useParams()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [categories, setCategories] = useState([])

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
  })

  useEffect(() => {
    loadProduct()
    loadCategories()
  }, [slug])

  const loadProduct = async () => {
    try {
      const { data } = await productsAPI.get(slug)

      setFormData({
        name: data.name || '',
        description: data.description || '',
        price: data.price || '',
        discount_price: data.discount_price || '',
        stock: data.stock || '',
        sku: data.sku || '',
        brand: data.brand || '',
        category: data.category?.id || '',
        is_featured: data.is_featured || false,
      })
    } catch {
      toast.error('Failed to load product')
    } finally {
      setLoading(false)
    }
  }

  const loadCategories = async () => {
    try {
      const { data } = await productsAPI.categories()
      setCategories(data.results || data)
    } catch {
      toast.error('Failed to load categories')
    }
  }

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
      setSaving(true)

      await productsAPI.update(slug, {
        ...formData,
        category: Number(formData.category),
      })

      toast.success('Product updated successfully')

      navigate('/admin/products')
    } catch {
      toast.error('Failed to update product')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="p-8">Loading...</div>

 return (
  <div className="max-w-4xl mx-auto px-4 py-8">
    <h1 className="text-2xl font-bold mb-6">
      Edit Product
    </h1>

    <form
      onSubmit={handleSubmit}
      className="card p-6 space-y-4"
    >
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Product Name"
        className="input-field"
      />

      <textarea
        name="description"
        value={formData.description}
        onChange={handleChange}
        rows="4"
        className="input-field"
        placeholder="Description"
      />

      <div className="grid md:grid-cols-2 gap-4">
        <input
          name="price"
          type="number"
          value={formData.price}
          onChange={handleChange}
          placeholder="Price"
          className="input-field"
        />

        <input
          name="discount_price"
          type="number"
          value={formData.discount_price}
          onChange={handleChange}
          placeholder="Discount Price"
          className="input-field"
        />

        <input
          name="stock"
          type="number"
          value={formData.stock}
          onChange={handleChange}
          placeholder="Stock"
          className="input-field"
        />

        <input
          name="sku"
          value={formData.sku}
          onChange={handleChange}
          placeholder="SKU"
          className="input-field"
        />

        <input
          name="brand"
          value={formData.brand}
          onChange={handleChange}
          placeholder="Brand"
          className="input-field"
        />

        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
          className="input-field"
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

      <label className="flex items-center gap-2">
        <input
          type="checkbox"
          name="is_featured"
          checked={formData.is_featured}
          onChange={handleChange}
        />
        Featured Product
      </label>

      <button
        type="submit"
        disabled={saving}
        className="btn-primary"
      >
        {saving ? 'Updating...' : 'Update Product'}
      </button>
    </form>
  </div>
)
}