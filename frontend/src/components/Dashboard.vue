<template>

  <div class="container-fluid">
    <div class="row">
      <div id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-body-tertiary sidebar collapse overflow-auto">

        <div class="card rounded-0">
          <div class="card-header">Sensor Type</div>
          <div class="card-body">
            <div class="form-check" v-for="(type, index) in this.radiobuttonsTypes" :key="index">
              <input class="form-check-input" type="radio" :id="'type' + index" :value="type.value"
                     v-model="selectedType">
              <label class="form-check-label" :for="'type' + index">{{ type.label }}
              </label>
            </div>
          </div>
        </div>

        <div class="card rounded-0">
          <div class="card-header">
            Metrics
            <div class="btn-group btn-group-sm" role="group" aria-label="Select/deselect all metrics">
              <button type="button" class="btn btn-outline-primary" @click="includeAllMetrics">All</button>
              <button type="button" class="btn btn-outline-primary" @click="excludeAllMetric">None</button>
            </div>
          </div>
          <div class="card-body">
            <div class="form-check" v-for="(metric, index) in this.checkboxMetrics" :key="index">
              <input class="form-check-input" type="checkbox" :id="'metric' + index" :value="metric"
                     v-model="selectedMetrics">
              <label class="form-check-label" :for="'metric' + index">{{ metric }}</label>
            </div>
          </div>
        </div>

      </div>


      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="table-responsive">

          <table class="table table-striped table-sm" v-if="filteredData.length">
            <thead>
            <tr>
              <th scope="col" v-for="key in this.columns"
                  @click="sortBy(key)"
                  :class="{ 'hidden': key !== 'sensor_name' && !selectedMetrics.includes(key), active: sortKey === key }">
                {{ capitalize(key) }}
                <span v-if="sortKey === key" class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'"></span>
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="entry in filteredData">
              <td v-for="key in this.columns"
                  :class="{ 'hidden': key !== 'sensor_name' && !selectedMetrics.includes(key)}">
                {{ entry[key] }}
              </td>
            </tr>
            </tbody>
          </table>

          <section class="py-5 text-center container" v-else>
            <div class="row py-lg-5">
              <div class="col-lg-6 col-md-8 mx-auto">
                <p v-if="stateLoading" class="lead">{{ stateLoading }}</p>
                <p v-else-if="stateConnectionError" class="lead">{{ stateConnectionError }}</p>
                <p v-else class="lead">No data satisfies the search criteria</p>
              </div>
            </div>
          </section>

        </div>
      </main>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import config from '../config.js'
import '../assets/dashboard.css'


export default {
  props: {
    filterPattern: String
  },
  data() {
    return {
      sortKey: '',
      sortOrders: [],
      tableData: [],
      selectedType: 'ALL',
      checkboxMetrics: [],
      selectedMetrics: [],
      stateLoading: false,
      stateConnectionError: '',
      radiobuttonsTypes: [],
    }
  },
  computed: {
    filteredData() {
      const sortKey = this.sortKey
      const filterPattern = this.filterPattern && this.filterPattern.toLowerCase()
      const order = this.sortOrders[sortKey] || 1
      let data = this.tableData

      if (this.selectedType !== 'ALL') {
        data = data.filter((row) => {
          return String(row['sensor_type_version_name']) === this.selectedType
        })
      }

      if (filterPattern) {
        data = data.filter((row) => {
          return String(row['sensor_name']).toLowerCase().indexOf(filterPattern) > -1
        })
      }
      if (sortKey) {
        data = data.slice().sort((a, b) => {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
    }
  },

  mounted() {
    this.stateLoading = 'Loading...'
    axios.get(config.apiUrl, {timeout: 5000})
        .then(response => {
          this.tableData = response.data.data
          this.columns = response.data.columns
          this.types = response.data.types
          this.radiobuttonsTypes = this.types.map((type) => {
            return {
              label: type,
              value: type
            }
          })
          this.checkboxMetrics = response.data.metrics
          this.selectedMetrics = config.selectedMetricDefault

          if (Array.isArray(config.selectedMetricDefault)) {
            this.selectedMetrics = config.selectedMetricDefault
            if (config.selectedMetricDefault.includes('All')) {
              this.selectedMetrics = this.checkboxMetrics
            } else if (config.selectedMetricDefault.includes('None')) {
              this.selectedMetrics = []
            }
          }

          this.sortOrders = this.columns.reduce((o, key) => ((o[key] = 1), o), {})
        })
        .catch(error => {
          console.log(error)
          this.stateConnectionError = 'No connection to the backend'
        })
        .finally(() => {
          this.stateLoading = false
        })
  },

  methods: {
    sortBy(key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    },

    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },

    includeAllMetrics() {
      this.selectedMetrics = this.checkboxMetrics
    },

    excludeAllMetric() {
      this.selectedMetrics = []
    },

  },
}
</script>


<style>

th.hidden, td.hidden {
  display: none;
}

th[scope="col"] {
  user-select: none;
  cursor: default;
}

th.active {
  color: var(--bs-primary);
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 1;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid var(--bs-primary);
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid var(--bs-primary);
}
</style>
