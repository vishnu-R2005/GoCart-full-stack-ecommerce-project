import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import { wishlistAPI } from '../services/api'
import ProductCard from '../components/products/ProductCard'
import { ProductGridSkeleton } from '../components/common/Skeleton'

export default function Wishlist() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadWishlist()
  }, [])

  const loadWishlist = async () => {
    try {
      const { data } = await wishlistAPI.list()
      setItems(data.results || [])
    } catch {
      toast.error('Failed to load wishlist')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <ProductGridSkeleton />
      </div>
    )
  }

  if (items.length === 0) {
    return (
      <div className="text-center py-16">
        <h2 className="text-2xl font-bold">
          Your wishlist is empty
        </h2>
      </div>
    )
  }
 return (
  <div className="max-w-7xl mx-auto px-4 py-8">
    <h1 className="text-2xl font-bold mb-6">
      My Wishlist
    </h1>

    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {items.map((item) => (
        <ProductCard
          key={item.id}
          product={item.product}
          isWishlistPage={true}
        />
      ))}
    </div>
  </div>

  )}