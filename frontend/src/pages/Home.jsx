import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { fetchFeatured } from '../store/slices/productsSlice'
import ProductCard from '../components/products/ProductCard'
import { ProductGridSkeleton } from '../components/common/Skeleton'

export default function Home() {
  const dispatch = useDispatch()
  const { featured } = useSelector((s) => s.products)

  useEffect(() => {
    dispatch(fetchFeatured())
  }, [dispatch])

  return (
    <div>
      <section className="bg-gradient-to-r from-gocart-dark to-gray-800 text-white py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Welcome to <span className="text-gocart-orange">GoCart</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8">Shop Smarter. Shop Faster.</p>
          <Link to="/products" className="btn-primary text-lg px-8 py-3 inline-block">
            Shop Now
          </Link>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 py-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">Featured Products</h2>
          <Link to="/products" className="text-gocart-orange hover:underline">View All →</Link>
        </div>
        {featured.length === 0 ? (
          <ProductGridSkeleton />
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {featured.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        )}
      </section>

      <section className="bg-primary-50 dark:bg-gray-800 py-12">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          {[
            { icon: '🚚', title: 'Fast Delivery', desc: 'Quick shipping across India' },
            { icon: '🔒', title: 'Secure Payments', desc: 'Razorpay powered checkout' },
            { icon: '↩️', title: 'Easy Returns', desc: 'Hassle-free return policy' },
          ].map((f) => (
            <div key={f.title} className="card p-6">
              <div className="text-4xl mb-3">{f.icon}</div>
              <h3 className="font-bold text-lg">{f.title}</h3>
              <p className="text-gray-500 dark:text-gray-400 mt-1">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
