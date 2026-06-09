import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import toast from 'react-hot-toast'
import { addToCart } from '../../store/slices/cartSlice'
import { wishlistAPI } from '../../services/api'

export default function ProductCard({ product }) {
  const dispatch = useDispatch()
  const { isAuthenticated } = useSelector((s) => s.auth)

  const handleAddToCart = async (e) => {
    e.preventDefault()
    if (!isAuthenticated) {
      toast.error('Please login to add items to cart')
      return
    }
    try {
      await dispatch(addToCart({ productId: product.id, quantity: 1 })).unwrap()
      toast.success('Added to cart!')
    } catch {
      toast.error('Failed to add to cart')
    }
  }

  const handleWishlist = async (e) => {
    e.preventDefault()
    if (!isAuthenticated) {
      toast.error('Please login first')
      return
    }
    try {
      await wishlistAPI.add(product.id)
      toast.success('Added to wishlist!')
    } catch {
      toast.error('Failed to add to wishlist')
    }
  }

  return (
    <Link to={`/products/${product.slug}`} className="card overflow-hidden hover:shadow-lg transition-shadow group">
      <div className="relative aspect-square bg-gray-100 dark:bg-gray-700">
        {product.primary_image ? (
          <img src={product.primary_image} alt={product.name} className="w-full h-full object-cover" loading="lazy" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">No Image</div>
        )}
        {product.discount_percentage > 0 && (
          <span className="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded">
            -{product.discount_percentage}%
          </span>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-medium text-sm line-clamp-2 group-hover:text-gocart-orange">{product.name}</h3>
        <div className="flex items-center gap-1 mt-1">
          <span className="text-yellow-500 text-sm">★ {product.avg_rating}</span>
          <span className="text-gray-400 text-xs">({product.reviews_count})</span>
        </div>
        <div className="flex items-baseline gap-2 mt-2">
          <span className="text-lg font-bold">₹{product.effective_price}</span>
          {product.discount_price && (
            <span className="text-sm text-gray-400 line-through">₹{product.price}</span>
          )}
        </div>
        <div className="flex gap-2 mt-3">
          <button onClick={handleAddToCart} className="btn-primary flex-1 text-sm py-1.5">
            Add to Cart
          </button>
          <button onClick={handleWishlist} className="btn-secondary px-3" aria-label="Add to wishlist">
            ♥
          </button>
        </div>
      </div>
    </Link>
  )
}
