import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { productsAPI } from '../../services/api'

export const fetchProducts = createAsyncThunk('products/list', async (params) => {
  const { data } = await productsAPI.list(params)
  return data
})

export const fetchFeatured = createAsyncThunk('products/featured', async () => {
  const { data } = await productsAPI.featured()
  return data.results
})

const productsSlice = createSlice({
  name: 'products',
  initialState: {
    list: [],
    featured: [],
    count: 0,
    loading: false,
    filters: { search: '', category: '', ordering: '-created_at' },
  },
  reducers: {
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => { state.loading = true })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false
        state.list = action.payload.results
        state.count = action.payload.count
      })
      .addCase(fetchFeatured.fulfilled, (state, action) => {
        state.featured = action.payload
      })
  },
})

export const { setFilters } = productsSlice.actions
export default productsSlice.reducer
