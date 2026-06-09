import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { cartAPI } from '../../services/api'

export const fetchCart = createAsyncThunk('cart/fetch', async (_, { rejectWithValue }) => {
  try {
    const { data } = await cartAPI.get()
    return data
  } catch (err) {
    return rejectWithValue(err.response?.data)
  }
})

export const addToCart = createAsyncThunk('cart/add', async ({ productId, quantity }, { rejectWithValue }) => {
  try {
    await cartAPI.add(productId, quantity)
    const { data } = await cartAPI.get()
    return data
  } catch (err) {
    return rejectWithValue(err.response?.data)
  }
})

export const removeFromCart = createAsyncThunk('cart/remove', async (productId, { rejectWithValue }) => {
  try {
    await cartAPI.remove(productId)
    const { data } = await cartAPI.get()
    return data
  } catch (err) {
    return rejectWithValue(err.response?.data)
  }
})

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    subtotal: 0,
    tax: 0,
    discount: 0,
    total: 0,
    itemCount: 0,
    loading: false,
  },
  reducers: {
    clearCartState: (state) => {
      state.items = []
      state.subtotal = 0
      state.tax = 0
      state.total = 0
      state.itemCount = 0
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCart.fulfilled, (state, action) => {
        state.items = action.payload.items || []
        state.subtotal = action.payload.subtotal
        state.tax = action.payload.tax
        state.discount = action.payload.discount
        state.total = action.payload.total
        state.itemCount = action.payload.item_count
        state.loading = false
      })
      .addCase(addToCart.fulfilled, (state, action) => {
        state.items = action.payload.items || []
        state.itemCount = action.payload.item_count
        state.total = action.payload.total
      })
      .addCase(removeFromCart.fulfilled, (state, action) => {
        state.items = action.payload.items || []
        state.itemCount = action.payload.item_count
        state.total = action.payload.total
      })
  },
})

export const { clearCartState } = cartSlice.actions
export default cartSlice.reducer
