'use strict';

var gulp = require('gulp');
var del = require('del');
var sass = require('gulp-sass');

// ====

var schedulePath = './core/static/schedule';

var configObj = {
  outputStyle: 'compressed'
};

// ====

gulp.task('sass', function () {
  return gulp.src(schedulePath + '/sass/**/*.scss')
    .pipe(sass(configObj).on('error', sass.logError))
    .pipe(gulp.dest(schedulePath + '/css'));
});

gulp.task('clean', function() {
  return del([
    schedulePath + '/css'
  ])
});

gulp.task('sass:watch', function () {
  gulp.watch(schedulePath + '/sass/**/*.scss', [
    'clean',
    'sass'
  ]);
});
