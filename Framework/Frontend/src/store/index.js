import { createStore } from 'vuex'
import * as d3 from "d3"
export default createStore({
  state: {
    dataset: [],
    bell: 0
  },
  getters:{ /* Define how different views access the global data. */
    dataset(state) {
      return state.dataset
    },
    realm(state) {
      return state.dataset.filter((v) => v.selected)
    },
    focus(state) {
      return state.dataset.filter((v) => v.grandfathered)
    },
    bell(state) {
      return state.bell
    }
  },
  mutations: { /* Change state value */
    update(state, payload) {
      state[payload.field] = payload.data
    },
    simpleNotify (state) {
      state.bell ++
    }
  },
  actions: {  /* Invoke functions; only functions here can use mutations */
    async getScatterDataset(context) {
      await d3.json('./dataset/dot_data.json').then(function(d) {
        context.commit('update', {
          field: 'dataset',
          data: d
        })
      })
    },
    notify(context) {
      context.commit('simpleNotify')
    }
  },
  modules: {
  }
})
