import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'
import { analyticsAPI } from '../services/api'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [monthlySales, setMonthlySales] = useState([])
  const [topProducts, setTopProducts] = useState([])
  const [recentOrders, setRecentOrders] = useState([])

  useEffect(() => {
    analyticsAPI.dashboard().then(({ data }) => setStats(data.stats))
    analyticsAPI.monthlySales().then(({ data }) => setMonthlySales(data.results || []))
    analyticsAPI.topProducts().then(({ data }) => setTopProducts(data.results || []))
    analyticsAPI.recentOrders().then(({ data }) => setRecentOrders(data.results || []))
  }, [])

  if (!stats) return <div className="max-w-7xl mx-auto px-4 py-8 animate-pulse"><div className="h-64 bg-gray-200 dark:bg-gray-700 rounded-xl" /></div>

  const statCards = [
    { label: 'Total Revenue', value: `₹${stats.total_revenue}`, color: 'text-green-600' },
    { label: 'Monthly Revenue', value: `₹${stats.monthly_revenue}`, color: 'text-blue-600' },
    { label: 'Total Orders', value: stats.total_orders, color: 'text-purple-600' },
    { label: 'Pending Orders', value: stats.pending_orders, color: 'text-yellow-600' },
    { label: 'Customers', value: stats.total_customers, color: 'text-indigo-600' },
    { label: 'Products', value: stats.total_products, color: 'text-orange-600' },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">GoCart Admin Dashboard</h1>
      <p className="text-gray-500 mb-8">Shop Smarter. Shop Faster.</p>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {statCards.map((s) => (
          <div key={s.label} className="card p-4 text-center">
            <p className="text-sm text-gray-500">{s.label}</p>
            <p className={`text-2xl font-bold mt-1 ${s.color}`}>{s.value}</p>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <div className="card p-6">
          <h3 className="font-bold mb-4">Monthly Sales</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={monthlySales}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" tickFormatter={(v) => new Date(v).toLocaleDateString('en', { month: 'short' })} />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#ff9900" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="card p-6">
          <h3 className="font-bold mb-4">Top Products</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={topProducts}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product_name" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total_sold" fill="#ff9900" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="font-bold mb-4">Recent Orders</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead><tr className="border-b"><th className="text-left py-2">Order</th><th className="text-left">Status</th><th className="text-right">Total</th><th className="text-right">Date</th></tr></thead>
            <tbody>
              {recentOrders.map((o) => (
                <tr key={o.id} className="border-b">
                  <td className="py-2">{o.order_number}</td>
                  <td className="capitalize">{o.status}</td>
                  <td className="text-right">₹{o.total}</td>
                  <td className="text-right">{new Date(o.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
