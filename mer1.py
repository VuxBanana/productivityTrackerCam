def detect_presence():
    cap = cv2.VideoCapture(0)
    excel_active = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Slika nije uspešno pročitana")
            continue
        
        cv2.imshow('frame', frame)
        
        if is_excel_active() and not excel_active:
            print("Korisnik gleda Excel")
            excel_active = True
            start_time = time.time()
        
        if excel_active and not is_excel_active():
            excel_active = False
            elapsed_time = time.time() - start_time
            print("Korisnik je prestao da gleda Excel.")
            print("Vreme provedeno gledajući Excel: ", elapsed_time, " sekundi")
        
        if excel_active:
            elapsed_time = time.time() - start_time
            print("Korisnik gleda Excel već: ", elapsed_time, " sekundi")
            
        # Provera da li je korisnik ispred kamere
        if excel_active and is_excel_active():
            elapsed_time = time.time() - start_time
            print("Korisnik je ispred kamere i gleda Excel već: ", elapsed_time, " sekundi")
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

detect_presence()