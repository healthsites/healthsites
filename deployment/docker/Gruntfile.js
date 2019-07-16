module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('/package.json'),

        requirejs: {
            compile: {
                options: {
                    optimize: 'none',
                    out: function(text, sourceMapText) {
                        var UglifyJS = require('uglify-es'),
                        uglified = UglifyJS.minify(text);
                        grunt.file.write('/home/web/django_project/frontend/static/scripts/configs/optimized.js', uglified.code);
                    },
                    baseUrl: '/home/web/django_project/frontend',
                    mainConfigFile: '/home/web/django_project/frontend/static/scripts/configs/index.js',
                    name: 'static/libs/almond/almond',
                    include: ['static/scripts/configs/index.js'],
                }
            }
        }

    });

    // Load plugins here.
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify-es');
    grunt.loadNpmTasks('grunt-contrib-requirejs');

    // Register tasks here.
    grunt.registerTask('default', ['requirejs']);
};
