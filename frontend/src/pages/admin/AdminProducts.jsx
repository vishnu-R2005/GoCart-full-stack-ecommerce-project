import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import { productsAPI } from '../../services/api'

export default function AdminProducts() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  const loadProducts = async () => {
    try {
      const { data } = await productsAPI.list({
        search,
        ordering: '-created_at'
      })

      setProducts(data.results || [])
    } catch {
      toast.error('Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProducts()
  }, [search])

  const handleDelete = async (slug) => {
    if (!window.confirm('Delete this product?')) return

    try {
      await productsAPI.delete(slug)

      toast.success('Product deleted')

      loadProducts()
    } catch {
      toast.error('Failed to delete product')
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        Loading...
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">

      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">
          Product Management
        </h1>

        <Link
          to="/admin/products/add"
          className="btn-primary"
        >
          Add Product
        </Link>
      </div>

      <input
        type="search"
        placeholder="Search products..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="input-field mb-6"
      />

      <div className="card overflow-hidden">
        <table className="w-full text-sm">

          <thead>
            <tr className="border-b">
              <th className="text-left p-3">Image</th>
              <th className="text-left p-3">Name</th>
              <th className="text-left p-3">Price</th>
              <th className="text-left p-3">Stock</th>
              <th className="text-left p-3">Status</th>
              <th className="text-right p-3">Actions</th>
            </tr>
          </thead>

          <tbody>
            {products.map((product) => (
              <tr
                key={product.id}
                className="border-b"
              >

                <td className="p-3">
                  {product.primary_image ? (
                    <img
                        src={product.primary_image}
                        alt={product.name}
                        className="w-12 h-12 object-cover rounded"
                        />
                  ) : (
                    'No Image'
                  )}
                </td>

                <td className="p-3">
                  {product.name}
                </td>

                <td className="p-3">
                  ₹{product.effective_price}
                </td>

                <td className="p-3">
                  {product.stock}
                </td>

                <td className="p-3">
                  {product.is_active ? 'Active' : 'Inactive'}
                </td>

                <td className="p-3 text-right">
                  <div className="flex justify-end gap-2">

                    <Link
                      to={`/admin/products/edit/${product.slug}`}
                      className="btn-secondary"
                    >
                      Edit
                    </Link>

                    <button
                      onClick={() =>
                        handleDelete(product.slug)
                      }
                      className="text-red-500"
                    >
                      Delete
                    </button>

                  </div>
                </td>

              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  )
}