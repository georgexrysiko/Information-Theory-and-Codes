# Information Theory and Codes

Η εργασία αυτή αποτελεί μια εφαρμογή τύπου client-server με στόχο τη μεταδόση, κωδικοποίηση/αποκωδικοποίηση και συμπίεση/αποσυμπίεση εικόνων.
Ο client συμπιέζει μια εικόνα χρησιμοποιώντας αλγόριθμο συμπίεσης Fano Shannon, προσθέτει padding σύμφωνα με το πρότυπο PKCS7, εφαρμόζει ορθογώνιο κώδικα για κωδικοποίηση, εισάγει σφάλματα και την στέλνει στον server.
Ο server στη συνέχεια επιδιώκει να επαναφέρει την εικόνα αποκωδικοποιώντας την, διορθώνοντας σφάλματα και αποσυμπιέζοντάς την.



## Αρχεία

* `client.py`: Εκτέλεση client side.
* `coding.py`: Υλοποίηση ορθογώνιου κώδικα Walsh-Hadamard για κωδικοποίηση και αποδικοποίηση.
* `fanoshannon.py`: Υλοποίηση αλγορίθμου συμπίεσης Fano Shannon για συμπίεση και αποσυμπίεση.
* `main.py`: Διαχείρηση και εκτέλεση.
* `server.py`: Εκτέλεση server side.
* `utils.py`: Βοηθητικές συναρτήσεις όπως υπολογισμός εντροπίας, έλεγχος MIME type, υπολογισμός SHA256, μετατροπή από και σε base64, προσθήκη σφαλμάτων, προσθήκη Padding PKCS7, μετρατροπή από bit σε byte και αντίστροφα.


## Εκτέλεση

1. Εκτέλεση μέσω `main.py`:
   * Για την εκτέλεση του server, τοποθετείτε το παρακάτω script σε ένα terminal:
     ```bash
     python main.py server
     ```
   * Για την εκτέλεση του client, τοποθετείτε το παρακάτω script σε ένα terminal:
     ```bash
     python main.py client
     ```
2. Εκτέλεση μέσω του κάθε script ξεχωριστά:
   * Για την εκτέλεση του server, τοποθετείτε το παρακάτω script σε ένα terminal:
     ```bash
     python server.py
     ```
   * Για την εκτέλεση του client, τοποθετείτε το παρακάτω script σε ένα terminal:
     ```bash
     python client.py
     ```
3. Εκτέλεση help manual
   * Για την εκτέλεση του manual, τοποθετείτε το παρακάτω script σε ένα terminal:
     ```bash
     python main.py
     ```

     Ή

     ```bash
     python main.py help
     ```

     
## Παραδείγματα εκτέλεσης

1. Εκτέλεση μέσω `main.py`
   * Εκκίνηση server
     ![image](https://github.com/user-attachments/assets/331e5903-6931-4505-9e50-bb4ce3f16267)
   * Εκκίνηση client
     ![image](https://github.com/user-attachments/assets/b5a51609-a169-47af-ab32-6979c9ad1910)
   * Εισαγωγή δεδομένων και αποτελέσματα
     * CLIENT
     ![image](https://github.com/user-attachments/assets/1ea2a9fc-d69e-4778-82b3-8d991a268ba3)
     * SERVER
     ![image](https://github.com/user-attachments/assets/4812a60f-2ee5-4638-88ef-68d7af34a398)

2. Ξεχωριστή εκτέλεση
   * Εκκίνηση server
     ![image](https://github.com/user-attachments/assets/1e71f143-68d4-4b64-8fad-44e3214548d4)
   * Εκκίνηση client
     ![image](https://github.com/user-attachments/assets/9595ef4d-74a2-438d-8ca2-d39469d33792)
   * Εισαγωγή δεδομένων και αποτελέσματα
     * CLIENT
     ![image](https://github.com/user-attachments/assets/68361c91-7e91-4217-8fcc-413a664bc441)
     * SERVER
     ![image](https://github.com/user-attachments/assets/1ad2f646-0d1c-4a47-b826-81155e887410)

3. Εκτέλεση help manual
   ![image](https://github.com/user-attachments/assets/adcf3e0f-f6ce-427c-a988-a582890a73e0)




