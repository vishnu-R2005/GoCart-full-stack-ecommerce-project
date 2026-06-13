import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchProducts } from '../store/slices/productsSlice'
import ProductCard from '../components/products/ProductCard'
import { ProductGridSkeleton } from '../components/common/Skeleton'

export default function Products() {
  const dispatch = useDispatch()
  const { list, count, loading } = useSelector((s) => s.products)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)

  useEffect(() => {
    dispatch(fetchProducts({ search, page, ordering: '-created_at' }))
  }, [dispatch, search, page])

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <input
          type="search"
          placeholder="Search products..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1) }}
          className="input-field max-w-md"
        />
        <p className="text-gray-500 self-center">{count} products found</p>
      </div>

      {loading ? (
        <ProductGridSkeleton />
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {list.map((p) => <ProductCard key={p.id} product={p} />)}
        </div>
      )}

      {count > 12 && (
        <div className="flex justify-center gap-2 mt-8">
          <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary">Prev</button>
          <span className="self-center px-4">Page {page}</span>
          <button onClick={() => setPage((p) => p + 1)} className="btn-secondary">Next</button>
        </div>
      )}
    </div>
  )
}
