(ns russtress.prod
  (:require
    [russtress.envs :as envs]
    [russtress.core :as core]
    ))

;;ignore println statements in prod
(set! *print-fn* (fn [& _]))

(core/init!)
