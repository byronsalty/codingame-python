(ns Player
  (:gen-class))

; Auto-generated code below aims at helping you parse
; the standard input according to the problem statement.

(defn abs [x]
    (max x (* -1 x)))

(defn get-lands [N]
    (loop [i N
           acc []]
      (if (= i 0)
        acc
        (let [LAND_X (read) LAND_Y (read)] 
            (recur (dec i) (conj acc [LAND_X LAND_Y]))))))

(defn find-landing-spot [LANDS]
    (let [links (map vector LANDS (rest LANDS))]
         (first (filter (fn [link] (if (= (second (first link)) (second (second link))) true false))
                 links))))
             
(defn get-turns-left [vs vdist]
    (if (= 0 vs)
        100
        (quot vdist (abs vs))))

(defn sign [x]
    (/ x (abs x)))
             
(def rotation-max [0 30 20 5])
             
(defn rotation-control [x hs vs mid ldist rdist vdist phase]
    
    (let [turns-left (min 40 (get-turns-left vs vdist))
          pred-landing (+ (* turns-left hs) x)
          dist (- pred-landing mid)]
            
        (binding [*out* *err*]
          (println "vs: " vs)
          (println "turns: " turns-left)
          (println "mid: " mid)
          (println "pred-x: " pred-landing)
          (println "pred-dist: " dist)
          (println "vdist: " vdist))
      
        (if (or (< vdist (abs vs)) (= 0 (abs dist)))
            0
            (if (> (abs hs) 80)
                (* (sign hs) (min (nth rotation-max phase) (abs hs)))
                (* (sign dist)
                   (min (nth rotation-max phase) (quot (abs dist) 45)))))))
             
; phase 1 = target 0 vs
; phase 2 = target -25 vs
; phase 3 = target -15 vs
(def target-vs [0 0 -35 -15])

(defn should-increase [vs rotate p phase]
    (or (< vs (- (nth target-vs phase) 0)) (and (> (abs rotate) 10) (< p 3))))
        

(defn should-decrease [hs vs vdist rotate p phase]
    (if (= phase 1)
        (>= vs (+ (nth target-vs phase) 10))
        (>= (min hs vs) (+ (nth target-vs phase) 2))))
    
(defn power-control [target y hs vs vdist p rotate phase]
    (if (and (< p 4) (should-increase vs rotate p phase))
        (inc p)
        (if (and (should-decrease hs vs vdist rotate p phase) (> p 0))
            (dec p)
            p)))

(defn determine-phase [target x y hs vs vdist]
    "1 = get above, 2 = descend, 3 = land"
    (let [above (if (and (> x (first (first target))) (< x (first (second target)))) true false)]
         
        (binding [*out* *err*]
          (println "x: " x)
          (println "left: " (first (first target)))
          (println "right: " (second (first target)))
          (println "above: " above)
        )
         (if (not (and above (< (abs hs) 20)))
             1
             (if (> vdist 500)
                 2
                 3))))
     

(defn -main [& args]
  (let [N (read)
        LANDS (get-lands N)
        target (find-landing-spot LANDS)]
    ; N: the number of points used to draw the surface of Mars.
    
    (while true
      (let [X (read) Y (read) HS (read) VS (read) F (read) R (read) P (read)
            mid (/ (+ (first (first target)) (first (second target))) 2)
            mid-dist (- X mid)
            left-dist (- X (first (first target)))
            right-dist (- X (first (second target)))
            vdist (- Y (second (first target)))
            phase (determine-phase target X Y HS VS vdist)
            rotate (rotation-control X HS VS mid left-dist right-dist vdist phase)
            power (power-control target Y HS VS vdist P rotate phase)]
        ; HS: the horizontal speed (in m/s), can be negative.
        ; VS: the vertical speed (in m/s), can be negative.
        ; F: the quantity of remaining fuel in liters.
        ; R: the rotation angle in degrees (-90 to 90).
        ; P: the thrust power (0 to 4).
        
        (binding [*out* *err*]
          (println "xy: " X Y " speeds: " HS VS " fuel: " F " rota: " R " pow: " P)
          (println "phase: " phase)
          (println "target: " target)
          (println "lands: " LANDS))
        
        ; R P. R is the desired rotation angle. P is the desired thrust power.
        (println rotate power)))))
