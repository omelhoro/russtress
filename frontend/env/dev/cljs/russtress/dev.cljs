(ns ^:figwheel-no-load russtress.dev
  (:require
            [russtress.envs :as envs]
            [russtress.core :as core]
            [figwheel.client :as figwheel :include-macros true]))

(enable-console-print!)

(figwheel/watch-and-reload
  :websocket-url "ws://localhost:3449/figwheel-ws"
  :jsload-callback core/mount-root)
  (println "js/goog.DEBUGGIN: " envs/BACKEND-ENDPOINT)

(core/init!)
