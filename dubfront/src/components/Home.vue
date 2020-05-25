<template>
  <div class="home">
    <el-row display="margin-top:10px">
        <el-input v-model="input" placeholder="请输入秀秀ID" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" @click="addUser()" style="float:left; margin: 2px;">新增</el-button>
        <el-button type="primary" @click="showFilms()" style="float:left; margin: 2px;">搜索</el-button>
    </el-row>
    <el-row>
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
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
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
            // console.log(this.total)
          } else {
            this.$message.error('查询作品失败')
            console.log(res['msg'])
          }
        })
    },
    current_change: function (currentPage) {
      this.currentPage = currentPage
    }
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
  color: #42b983;
}
</style>
