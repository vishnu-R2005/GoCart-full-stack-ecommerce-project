import { getAccessToken } from '../utils/tokenStorage'
import axios from 'axios'
// import { store } from '../store'
// import { logout, setTokens } from '../store/slices/authSlice'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
})

// api.interceptors.request.use((config) => {
//   const token = store.getState().auth.accessToken
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`
//   }
//   return config
// })

// api.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const original = error.config
//     if (error.response?.status === 401 && !original._retry) {
//       original._retry = true
//       const refresh = store.getState().auth.refreshToken
//       if (refresh) {
//         try {
//           const { data } = await axios.post(`${API_URL}/accounts/token/refresh/`, { refresh })
//           store.dispatch(setTokens({ access: data.access, refresh }))
//           original.headers.Authorization = `Bearer ${data.access}`
//           return api(original)
//         } catch {
//           store.dispatch(logout())
//         }
//       }
//     }
//     return Promise.reject(error)
//   }
// )

api.interceptors.request.use((config) => {
  const token = getAccessToken()

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})
export default api

// Auth

export const authAPI = {
  register: (data) => api.post('/accounts/register/', data),
  login: (data) => api.post('/accounts/login/', data),
  logout: (refresh) => api.post('/accounts/logout/', { refresh }),
  profile: () => api.get('/accounts/profile/'),
  updateProfile: (data) => api.patch('/accounts/profile/', data),
  forgotPassword: (email) => api.post('/accounts/forgot-password/', { email }),
  resetPassword: (data) => api.post('/accounts/reset-password/', data),
  verifyEmail: (token) => api.post('/accounts/verify-email/', { token }),
  changePassword: (data) => api.post('/accounts/change-password/', data),
}

// Products
export const productsAPI = {
  list: (params) => api.get('/products/', { params }),
  get: (slug) => api.get(`/products/${slug}/`),
  featured: () => api.get('/products/featured/'),
  bestSellers: () => api.get('/products/best_sellers/'),
  related: (slug) => api.get(`/products/${slug}/related/`),
  categories: (tree = false) => api.get('/products/categories/', { params: tree ? { tree: true } : {} }),
  create: (data) => api.post('/products/', data),
  update: (slug, data) => api.patch(`/products/${slug}/`, data),
  delete: (slug) => api.delete(`/products/${slug}/`),
}

// Cart
export const cartAPI = {
  get: () => api.get('/cart/'),
  add: (productId, quantity = 1) => api.post('/cart/add/', { product_id: productId, quantity }),
  update: (productId, quantity) => api.patch(`/cart/update/${productId}/`, { quantity }),
  remove: (productId) => api.delete(`/cart/remove/${productId}/`),
  clear: () => api.delete('/cart/clear/'),
}

// Wishlist
export const wishlistAPI = {
  list: () => api.get('/products/wishlist/'),
  add: (productId) => api.post(`/products/wishlist/add/${productId}/`),
  remove: (productId) => api.delete(`/products/wishlist/remove/${productId}/`),
}

// Orders
export const ordersAPI = {
  list: () => api.get('/orders/'),
  get: (id) => api.get(`/orders/${id}/`),
  place: (data) => api.post('/orders/place/', data),
  cancel: (id) => api.post(`/orders/${id}/cancel/`),
  tracking: (id) => api.get(`/orders/${id}/tracking/`),
  applyCoupon: (code) => api.post('/orders/coupons/apply/', { code }),
}

// Payments
export const paymentsAPI = {
  createOrder: (orderId) => api.post('/payments/create_order/', { order_id: orderId }),
  verify: (data) => api.post('/payments/verify/', data),
}

// Addresses
export const addressesAPI = {
  list: () => api.get('/accounts/addresses/'),
  create: (data) => api.post('/accounts/addresses/', data),
  update: (id, data) => api.patch(`/accounts/addresses/${id}/`, data),
  delete: (id) => api.delete(`/accounts/addresses/${id}/`),
}

// Reviews
export const reviewsAPI = {
  list: (productId) => api.get('/products/reviews/', { params: { product: productId } }),
  create: (data) => api.post('/products/reviews/', data),
}

// Analytics
export const analyticsAPI = {
  dashboard: () => api.get('/analytics/dashboard/'),
  monthlySales: () => api.get('/analytics/monthly-sales/'),
  topProducts: () => api.get('/analytics/top-products/'),
  recentOrders: () => api.get('/analytics/recent-orders/'),
}

// Notifications
export const notificationsAPI = {
  list: () => api.get('/notifications/'),
  markRead: (id) => api.post(`/notifications/${id}/mark_read/`),
}

