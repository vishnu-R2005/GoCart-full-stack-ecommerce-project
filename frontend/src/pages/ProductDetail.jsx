import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import toast from 'react-hot-toast'
import { productsAPI } from '../services/api'
import { addToCart } from '../store/slices/cartSlice'
import ProductCard from '../components/products/ProductCard'

export default function ProductDetail() {
  const { slug } = useParams()
  const dispatch = useDispatch()
  const { isAuthenticated } = useSelector((s) => s.auth)
  const [product, setProduct] = useState(null)
  const [related, setRelated] = useState([])
  const [qty, setQty] = useState(1)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    productsAPI.get(slug).then(({ data }) => {
      setProduct(data)
      setLoading(false)
    })
    productsAPI.related(slug).then(({ data }) => setRelated(data.results || []))
  }, [slug])

  const handleAddToCart = async () => {
    if (!isAuthenticated) return toast.error('Please login first')
    await dispatch(addToCart({ productId: product.id, quantity: qty }))
    toast.success('Added to cart!')
  }

  if (loading) return <div className="max-w-7xl mx-auto px-4 py-8 animate-pulse"><div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-xl" /></div>
  if (!product) return <div className="text-center py-12">Product not found</div>

  const image = product.images?.[0]?.image || product.primary_image

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="grid md:grid-cols-2 gap-8">
        <div className="card aspect-square overflow-hidden">
          {image ? <img src={image} alt={product.name} className="w-full h-full object-cover" /> : <div className="flex items-center justify-center h-full text-gray-400">No Image</div>}
        </div>
        <div>
          <h1 className="text-3xl font-bold">{product.name}</h1>
          <p className="text-gray-500 mt-1">{product.brand} · {product.category_name}</p>
          <div className="flex items-center gap-2 mt-3">
            <span className="text-yellow-500">★ {product.avg_rating}</span>
            <span className="text-gray-400">({product.reviews_count} reviews)</span>
          </div>
          <div className="flex items-baseline gap-3 mt-4">
            <span className="text-3xl font-bold">₹{product.effective_price}</span>
            {product.discount_price && <span className="text-xl text-gray-400 line-through">₹{product.price}</span>}
          </div>
          <p className="mt-4 text-gray-600 dark:text-gray-300">{product.description}</p>
          <p className="mt-2 text-sm">{product.stock > 0 ? <span className="text-green-600">In Stock ({product.stock})</span> : <span className="text-red-500">Out of Stock</span>}</p>
          <div className="flex items-center gap-4 mt-6">
            <input type="number" min="1" max={product.stock} value={qty} onChange={(e) => setQty(+e.target.value)} className="input-field w-20" />
            <button onClick={handleAddToCart} disabled={product.stock === 0} className="btn-primary flex-1">Add to Cart</button>
          </div>
        </div>
      </div>

      {related.length > 0 && (
        <section className="mt-12">
          <h2 className="text-xl font-bold mb-4">Related Products</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {related.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>
      )}
    </div>
  )
}
