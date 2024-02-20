import { configureStore } from "@reduxjs/toolkit";
import { uiSlice } from "./features/uislice";

const store = configureStore({
    reducer: {
        ui: uiSlice.reducer,
    },
});

export default store;