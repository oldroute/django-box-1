let path = require('path');
const webpack = require('webpack');

const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const autoprefixer = require('autoprefixer');
const TerserPlugin = require('terser-webpack-plugin');
const ReplaceHashInFileWebpackPlugin = require('replace-hash-in-file-webpack-plugin');
const RenameWebpackPlugin = require('rename-webpack-plugin')
const FileManagerPlugin = require('filemanager-webpack-plugin');


let conf = {
    entry: {
        bundle: './lsnab/static/index.js',
        critical: './lsnab/static/critical.js',
    },
    output: {
        path: path.join(__dirname, './lsnab/static/bundle/'),
        filename: '[name].[hash].js',
        publicPath: '',
    },
    stats: {
        errors: true,
        errorDetails: true,
        builtAt: true,
        assets: false,
        modules: false,
        children: false,
    },
    optimization: {
        minimizer: [
            new TerserPlugin(),
            new OptimizeCSSAssetsPlugin({
                cssProcessor: require('cssnano'),
                cssProcessorPluginOptions: {
                    preset: ['default', { discardComments: { removeAll: true } }],
                },
            }),
        ],
    },
    module: {
        rules: [
            //js
            {
                test: /\.(js|jsx)$/,
                exclude: '/node_modules/',
                loader: 'babel-loader',
                query: {
                    cacheDirectory: true
                }
            },
            //sass
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    'style-loader',
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: [
                                autoprefixer({
                                    browsers:['last 20 versions']
                                })
                            ]
                        }
                    },

                    {
                        loader: 'sass-loader'
                    },
                ],
            },
            //image
            {
				test: /\.(png|jpg|jpeg|svg|gif)$/,
				use: [
					{
						loader: 'file-loader',
						options: {
							name: '../img/[name].[ext]'
						}
					}
				]
            }
        ],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            'window.jQuery': 'jquery'

        }),
        new MiniCssExtractPlugin({
            filename: "[name].[hash].css",
        }),
        new RenameWebpackPlugin({
            originNameReg: /critical.*.css/,
            targetName: 'critical.css'
        }),
        new ReplaceHashInFileWebpackPlugin([{
            dir: './lsnab/templates',
            files: ['base.html'],
            rules: [{
                search: /bundle\.*[a-zA-Z0-9]*\.js/,
                replace: 'bundle.[hash].js'
            },
            {
                search: /bundle\.*[a-zA-Z0-9]*\.css/,
                replace: 'bundle.[hash].css'
            }]
        }]),
        new FileManagerPlugin({
            onStart: [{
                delete: [
                 './lsnab/static/bundle/'
                ],
            }],
            onEnd: [{
                delete: [
                 './lsnab/static/bundle/critical.*.js'
                ],
                move: [
                    { source: './lsnab/static/bundle/critical.css', destination: './lsnab/templates/parts/critical.css' },
                ],
            }]
        })
    ]
};

module.exports = (env, options) => {
    let production = options.mode === 'production';

    conf.devtool = production 
                    ? false
                    : false;
    return conf;
}