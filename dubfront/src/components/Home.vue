<template>
  <div class="home">
  <v-card
    max-width="400"
    class="mx-auto"
  >
 <v-app-bar
      absolute
      color="teal lighten-3"
      dark
      hide-on-scroll
      prominent
      scroll-target="#scrolling-techniques-4"
    >
      <!-- <v-app-bar-nav-icon></v-app-bar-nav-icon> -->
      <v-toolbar-title>配音作品</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-col cols="6" sm="6" md="6">
       <v-text-field
          v-model="input"
          label="输入你的秀秀ID"
        ></v-text-field>
        </v-col>
      <v-btn icon  @click="addUser()">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
      <v-btn icon  @click="showFilms()">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <!-- <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn> -->
      <!-- <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn> -->
    </v-app-bar>
    <v-sheet
      id="scrolling-techniques-4"
      class="overflow-y-auto"
      max-height="1400"
    >
      <v-container style="height: 2000px;">
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
        <v-col cols="12">
          <v-card
            color="#385F73"
            dark
          >
            <v-card-title class="headline">Web版 秀秀作品集</v-card-title>
            <v-card-subtitle>不需要登录app，即可在web上观看作品，秀秀插件的第一步。</v-card-subtitle>
            <v-card-actions>
              <v-btn text>试试看</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col
          v-for="(item, i) in filmList"
          :key="i"
          cols="12"
        >
          <v-card
            :color=colorList[i*101%colorList.length]
            dark
          >
            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <a :href="item.fields.film_url">
                <v-card-title
                  class="headline"
                  v-text="item.fields.title"
                ></v-card-title>
                </a>
                <v-row justify="space-around">
                <v-card-subtitle v-text="item.fields.user"></v-card-subtitle>
                <v-avatar color="indigo" size="36">
                  <img
                    :src="item.fields.user_head"
                    :alt="item.fields.user"
                  >
                </v-avatar>
                </v-row>
              </div>

              <v-avatar
                class="ma-3"
                size="125"
                tile
              >
                <v-img :src="item.fields.image_url"></v-img>
              </v-avatar>
            </div>
          </v-card>
        </v-col>
      </v-row>
      </v-container>
    </v-sheet>
  </v-card>
    <!-- <el-row>
        <el-table :data="filmList.slice((currentPage-1)*pagesize,currentPage*pagesize)" style="width: 100%" border>
          <el-table-column prop="film_id" label="作品ID" min-width="20">
            <template slot-scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="title" label="作品名" min-width="40">
            <template slot-scope="scope"> {{ scope.row.fields.title }} </template>
          </el-table-column>
          <el-table-column prop="film_img" label="作品封面" min-width="100">
            <template slot-scope="scope">
              <a :href="scope.row.fields.film_url">
                <el-image
                  style="width: 162px; height: 100px"
                  :src= "scope.row.fields.image_url">
                </el-image>
              </a>
            </template>
          </el-table-column>
          <el-table-column prop="user_id" label="作者ID" min-width="30">
            <template slot-scope="scope"> {{ scope.row.fields.user }} </template>
          </el-table-column>
          <el-table-column prop="user_head" label="作者头像" min-width="15">
              <template slot-scope="scope">
              <el-avatar :src= "scope.row.fields.user_head" ></el-avatar>
              </template>
          </el-table-column>
          <el-table-column prop="play_count" label="播放量" min-width="20">
            <template slot-scope="scope"> {{ scope.row.fields.play_count }} </template>
          </el-table-column>
          <el-table-column prop="good_count" label="点赞数" min-width="20">
            <template slot-scope="scope"> {{ scope.row.fields.good_count }} </template>
          </el-table-column>
        </el-table>
        <div style="text-align: center;margin-top: 30px;">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="total"
            @current-change="current_change">
          </el-pagination>
        </div>
    </el-row>
    <VmImageList title="ImageList" data="filmList"></VmImageList> -->
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
      currentPage: 1
    }
  },
  mounted: function () {
    this.showFilms()
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
      this.$axios.get('http://127.0.0.1:8000/api/show_films?user_id=' + this.input)
        .then((res) => {
          res = res.data
          // console.log(res)
          if (res.error_num === 0) {
            this.filmList = res['films']
            this.total = this.filmList.length
            console.log(this.total)
          } else {
            this.$message.error('查询作品失败')
            console.log(res['msg'])
          }
        })
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
