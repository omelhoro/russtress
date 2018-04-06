(ns russtress.core
  (:require [reagent.core :as reagent :refer [atom]]
            [reagent.session :as session]
            [reagent.core :as r]
            [russtress.envs :as envs]
            [ajax.core :refer [GET POST]]
            [reagent.session :as session]
            [secretary.core :as secretary :include-macros true]
            [goog.events :as events]
            [goog.history.EventType :as EventType])
  (:import goog.History))

;; -------------------------
;; Views

(def text
  (atom
    "После распада Римской империи в Западной Европе образовалось Франкское государство, которое спустя три века, при Карле Великом, превратилось в империю (800 год). Империя Карла охватывала территории ряда современных государств, в частности Германии. Однако империя Карла Великого просуществовала недолго — внуки этого императора поделили её между собою, в результате чего образовались три королевства — Западнофранкское (впоследствии Франция), Восточнофранкское (впоследствии Германия) и Срединное королевство (вскоре распавшееся на Италию, Прованс и Лотарингию)."
    ))

(enable-console-print!)

(println "js/goog.DEBUG: " envs/BACKEND-ENDPOINT)

(def text-done
  (atom ""))

(def textarea-style {:height 300 :width "100%"})

(def rus-vowels (js/RegExp. "[иеаоуяюыёэИЕАОУЯЮЫЁЭ]" "i"))

(defn process-word [k v]
  (let [first-stress (first v)
        i-vow (first first-stress)
        i (atom 1)
        replace-fn (fn [v]
                     (if
                       (= @i i-vow)
                       (do (swap! i #(+ @i 1)) (str "'" v))
                       (do (swap! i #(+ @i 1)) v)
                       ))
        ]
    (if (> i-vow 100)
      k
      (clojure.string/replace k rus-vowels replace-fn)
      )
    )
  )

(process-word "Италию" [[2 "lem-stress"]])

(defn process-text []
  (let [
        text-tokenized (clojure.string/split @text #"([\u2000-\u206F\u2E00-\u2E7F\'!\"#\$%&\(\)\*\+,\-\.\/:;<=>\?@\[\]\^_`\{\|\}~ \n»«])")
        text-set (set text-tokenized)
        callback (fn [res]
                   (let [
                         stress-map (reduce-kv (fn [a k v] (assoc a k (process-word k v))) {} res)
                         stressed-text (map #(get stress-map % %) text-tokenized)
                         done (apply str stressed-text)
                         ]
                     (do
                       (print done)
                       (swap! text-done #(-> done))
                       )
                     )
                   )
        ]
    (POST (str envs/BACKEND-ENDPOINT "/stress")
          {:params          {:words text-set}
           :format          :json
           :response-format :json
           :handler         callback})
    )
  )

(defn app-body []
  [:div#app-body
   [:textarea.form-control {:value @text :on-change (fn [evt] (do (swap! text #(-> evt .-target .-value)))) :style textarea-style}]

   [:div
    {:style {:margin "10px auto" :display "table"}}
    [:button.btn-lg.btn-success {:on-click process-text} "Process"]
   ]

   [:textarea.form-control {:value @text-done :style textarea-style}]
   [:div.well
    {:style {:margin-top "5px"}}
    [:span {:style {:font-size "large"}} [:a {:href "https://home.fischerops.com"} "See more apps from me"]]
   ]
   ]
  )

(defn home-page []
  [:div
   [:div.jumbotron {:style {:text-align "center"}}
    [:h1 "Russtress"]
    [:h3 "Welcome to the automatic stress setter of Russian. It has 95% correctness. Just type in a text and click 'Process'"
     [:br ""]
     ]
    ]
   (app-body)
   ]
  )

(defn about-page []
  [:div [:h2 "About rustress"]
   [:div [:a {:href "#/"} "go to the home page"]]])

(defn current-page []
  [:div [(session/get :current-page)]])

;; -------------------------
;; Routes
(secretary/set-config! :prefix "#")

(secretary/defroute "/" []
                    (session/put! :current-page #'home-page))

;; -------------------------
;; History
;; must be called after routes have been defined
(defn hook-browser-navigation! []
  (doto (History.)
    (events/listen
      EventType/NAVIGATE
      (fn [event]
        (secretary/dispatch! (.-token event))))
    (.setEnabled true)))

;; -------------------------
;; Initialize app
(defn mount-root []
  (reagent/render [current-page] (.getElementById js/document "app")))

(defn init! []
  (hook-browser-navigation!)
  (mount-root))
