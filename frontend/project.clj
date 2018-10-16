(defproject russtress "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}

  :dependencies [[org.clojure/clojure "1.9.0"]
                 [ring-server "0.5.0"]
                 [reagent "0.8.2-SNAPSHOT"]
                 [cljs-ajax "0.7.5"]
                 [reagent-forms "0.5.43"]
                 [reagent-utils "0.3.1"]
                 [ring "1.7.0"]
                 [ring/ring-defaults "0.3.2"]
                 [prone "1.6.1"]
                 [compojure "1.6.1"]
                 [hiccup "1.0.5"]
                 [environ "1.0.2"]
                 [org.clojure/clojurescript "1.10.339" :scope "provided"]
                 [secretary "1.2.3"]
                 ]

  :plugins [[lein-environ "1.0.1"]
            [lein-asset-minifier "0.2.2"]
            [lein-cljsbuild "1.1.0"]
            [lein-ancient "0.6.15"]
            [com.cemerick/clojurescript.test "0.3.3"]
            ]

  :ring {:handler russtress.handler/app
         :uberwar-name "russtress.war"}

  :min-lein-version "2.5.0"

  :uberjar-name "russtress.jar"

  :clean-targets ^{:protect false} [:target-path
                                    [:cljsbuild :builds :app :compiler :output-dir]
                                    [:cljsbuild :builds :app :compiler :output-to]]

  :minify-assets
  {:assets
    {"resources/public/css/site.min.css" "resources/public/css/site.css"}}

  :cljsbuild {:builds {:app {:source-paths []
                             :compiler {:output-to     "resources/public/js/app.js"
                                        :output-dir    "resources/public/js/out"
                                        :asset-path   "js/out"
                                        :optimizations :none
                                        :pretty-print  true}}
                       }}

  :profiles {:dev {:repl-options {:init-ns russtress.repl}

                   :dependencies [[ring/ring-mock "0.3.2"]
                                  [ring/ring-devel "1.7.0"]
                                  [org.clojure/tools.nrepl "0.2.13"]
                                  [com.cemerick/piggieback "0.2.2"]
                                  [pjstadig/humane-test-output "0.8.3"]]
                  :plugins [
                    [lein-figwheel "0.5.16"]
                  ]

                   :source-paths ["env/dev/clj", "env/dev/cljs"]

                   :injections [(require 'pjstadig.humane-test-output)
                                (pjstadig.humane-test-output/activate!)]

                   :figwheel {:http-server-root "public"
                              :server-port 3449
                              :nrepl-port 7002
                              :nrepl-middleware ["cemerick.piggieback/wrap-cljs-repl"
                                                 ]
                              :css-dirs ["resources/public/css"]
                              }

                   :env {:dev true}

                   :cljsbuild {:builds {:app {:source-paths ["env/dev/cljs" "src/cljs"]
                                              :compiler {:main "russtress.dev"
                                                         :source-map true}}
                                        :test {:source-paths ["env/dev/cljs"  "src/cljs" "src/cljc" "test/cljs"]
                                               :compiler {:output-to "target/test.js"
                                                          :optimizations :whitespace
                                                          :pretty-print true}}

                                        }
                               :test-commands {"unit" ["phantomjs" :runner
                                                       "test/vendor/es5-shim.js"
                                                       "test/vendor/es5-sham.js"
                                                       "test/vendor/console-polyfill.js"
                                                       "target/test.js"]}
                               }}

             :uberjar {:hooks [leiningen.cljsbuild minify-assets.plugin/hooks]
                       :env {:production true}
                       :aot :all
                       :omit-source true
                       :cljsbuild {:jar true
                                   :builds {:app
                                             {:source-paths ["env/prod/cljs" "src/cljs"]
                                              :compiler
                                              {:optimizations :advanced
                                               :pretty-print false}}
                                             :server {}
                                            }}}})
