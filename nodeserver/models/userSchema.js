import mongoose from 'mongoose';

const reviewSchema = new mongoose.Schema({
  // title: {
  //   type: String,
  //   required: true,
  // },
  rating: {
    type: String,
    required: true,
  },
  star: {
    type: Number,
    required: true,
  },
  body: {
    type: String,
    required: true,
  },
  fullDate: {
    type: String,
    required: true,
  },
  date: {
    type: String,
    required: true,
  },
})

const sentimentSchema = new mongoose.Schema({
  negative: {
    type: Number,
    required: true,
  },
  neutral: {
    type: Number,
    required: true,
  },
  positive: {
    type: Number,
    required: true,
  },
})

const keywordSchema = new mongoose.Schema({
  word: {
    type: String,
    required: true,
  },
  score: {
    type: Number,
    required: true,
  },
})

const svaSchema = new mongoose.Schema({
  date: {
    type: String,
    required: true,
  },
  score: {
    type: Number,
    required: true,
  },
})

const productSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  url: {
    type: String,
    required: true,
  },
  price: {
    type: String,
    required: true,
  },
  image: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  reviews: [reviewSchema],
  sentiment: sentimentSchema,
  keywords: [keywordSchema],
  sva: [svaSchema]
});

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique:true,
  },
  phone: {
    type: Number,
    required: false,
  },
  password: {
    type: String,
    required: true,
  },
  products: [productSchema]
});

const User = mongoose.model("cres_user", userSchema);

export default User;