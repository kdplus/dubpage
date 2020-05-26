<template>
  <div class="home">
  <v-card
    class="mx-auto"
  >
    <v-app-bar
      dark
      color="pink"
    >
      <v-toolbar-title>配音作品</v-toolbar-title>
      <v-spacer></v-spacer>
        <v-col cols="6" sm="6">
          <v-text-field
            label="输入你的秀秀ID"
            single-line
            v-model="input"
          ></v-text-field>
        </v-col>
      <v-btn icon  @click="addUser()">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
      <v-btn icon  @click="showFilms()">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>

    <v-sheet
      id="scrolling-techniques-4"
      class="overflow-y-auto"
      max-height="1500"
    >
      <v-container style="height: 1500px;">
      <v-row dense>
        <v-col cols="12">
          <v-card
            color="#385F73"
            dark
          >
            <v-card-title class="headline">Web版 秀秀作品集</v-card-title>
            <v-card-subtitle>不需要登录app，即可在web上观看作品，秀秀插件的第一步。</v-card-subtitle>
          </v-card>
        </v-col>
        <!-- <v-btn
  class="md-5 mr-3 elevation-21"
  dark
  fab
  button
  right
  color="indigo darken-3"
  fixed
  @click="top"
></v-btn> -->
          <!-- <v-lazy
            v-model="isActive"
            :options="{
              threshold: .5
            }"
            min-height="1000"
            transition="fade-transition"
          > -->
        <!-- <v-col cols="12"> -->
        <v-col
          v-for="(item, i) in filmList"
          :key="i"
          cols="12"
        >
        <v-card
          max-width="1000"
          class="mx-auto"
        >
          <v-list-item>
            <v-list-item-avatar color="grey">
              <v-img :src="item.fields.user_head">
              </v-img>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="headline">{{item.fields.title}}</v-list-item-title>
              <v-list-item-subtitle>{{item.fields.user}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <a :href="item.fields.film_url">
          <v-img
            :src="item.fields.image_url"
            height="224"
          ></v-img>
          </a>
          <!-- <v-card-text>
            Visit ten places on our planet that are undergoing the biggest changes today.
          </v-card-text>

          <v-card-actions>
            <v-btn
              text
              color="deep-purple accent-4"
            >
              Read
            </v-btn>
            <v-btn
              text
              color="deep-purple accent-4"
            >
              Bookmark
            </v-btn> -->
            <v-spacer></v-spacer>
            <v-btn icon>
              <v-icon>mdi-heart</v-icon>
            </v-btn>
            <v-btn icon>
              <v-icon>mdi-share-variant</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
        </v-col>
        <!-- </v-col> -->
        <!-- </v-lazy> -->

      </v-row>
      </v-container>
    </v-sheet>
  </v-card>
      <!-- <v-btn
        color="pink"
        dark
        small
        absolute
        bottom
        left
        fab
      >
<v-icon v-if="btnFlag" class="go-top" @click="backTop"> mdi-plus </v-icon>
    </v-btn> -->
  </div>
</template>

<script>
import VmImageList from '@/components/vm-image-list'
export default {
  name: 'home',
  components: {
    VmImageList
  },
  data () {
    // return {
    //   input: '',
    //   filmList: [],
    //   multipleSelection: [],
    //   total: 0,
    //   pagesize: 10,
    //   currentPage: 1
    return {
      colorList: ['#133337', '#420420', '#800080', '#003366', '#660066', '#990000', '#ff4040'],
      input: '',
      filmList: [],
      multipleSelection: [],
      total: 0,
      pagesize: 10,
      isActive: false,
      currentPage: 0,
      noData: false,
      update: true
    }
  },
  mounted: function () {
    this.showFilms()
    this.scroll()
    window.addEventListener('scroll', this.scrollToTop)
  },
  destroyed () {
    window.removeEventListener('scroll', this.scrollToTop)
  },

  methods: {
    addUser () {
      console.log(this.input)
      this.$axios.get('http://127.0.0.1:8000/api/add_user?user_id=' + this.input)
        .then((res) => {
          // console.log(res)
          res = res.data
          if (res.error_num === 0) {
            this.$message('用户更新成功')
            this.showFilms()
          } else {
            this.$message.error('用户更新失败，请重试')
            console.log(res['msg'])
          }
        })
    },
    showFilms () {
      if (this.update === true) {
        this.currentPage = 0
        this.noData = false
      }
      this.$axios.get('http://127.0.0.1:8000/api/show_films?user_id=' + this.input + '&page=' + this.currentPage)
        .then((res) => {
          res = res.data
          // console.log(res)
          if (res.error_num === 0) {
            if (res['films'].length === 0) {
              this.noData = true
            } else {
              if (this.update === false) {
                this.filmList = this.filmList.concat(res['films'])
              } else {
                this.filmList = res['films']
              }
              this.total = this.filmList.length
            }
            console.log(this.update, this.filmList, this.total, res['films'].length)
            this.update = true
          } else {
            console.log(res['msg'])
            this.$message.error('查询作品失败')
            this.update = true
          }
        })
    },
    scroll () {
      let isLoading = false
      window.onscroll = () => {
        let bottomOfWindow = document.documentElement.offsetHeight - document.documentElement.scrollTop - window.innerHeight <= 200
        if (bottomOfWindow && isLoading === false && this.noData === false) {
          isLoading = true
          // axios.get(`https://randomuser.me/api/`).then(response => {
          //   person.push(response.data.results[0])
          //   isLoading = false
          // })
          this.currentPage += 1
          this.update = false
          this.showFilms()
          console.log('Yes')
          isLoading = false
        }
      }
    },
    top () {
      window.scrollTo(0, 0)
    },

    backTop () {
      const that = this
      let timer = setInterval(() => {
        let ispeed = Math.floor(-that.scrollTop / 5)
        document.documentElement.scrollTop = document.body.scrollTop = that.scrollTop + ispeed
        if (that.scrollTop === 0) {
          clearInterval(timer)
        }
      }, 16)
    },

    // 为了计算距离顶部的高度，当高度大于60显示回顶部图标，小于60则隐藏
    scrollToTop () {
      const that = this
      let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
      that.scrollTop = scrollTop
      if (that.scrollTop > 0) {
        that.btnFlag = true
      } else {
        that.btnFlag = false
      }
    },
    beforeMount () {
      // 在页面挂载前就发起请求
      this.showFilms()
    }
    // current_change: function (currentPage) {
    //   this.currentPage = currentPage
    // }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #d3dfda;
  text-decoration: none;
}
</style>
