from general_func import *


def header_gen(path):

    # Load the images and preprocess them for inception-resnet
    images = []
    all_filenames = listdir('images/header/') #header/ footer images
    all_filenames.sort()
    for filename in all_filenames:
        images.append(img_to_array(load_img('images/header/'+filename, target_size=(299, 299)))) #header/ footer images
    images = np.array(images, dtype=float)
    images = preprocess_input(images)

    # Run the images through inception-resnet and extract the features without the classification layer
    IR2 = InceptionResNetV2(weights='imagenet', include_top=False)
    features = IR2.predict(images)

    # We will cap each input sequence to 100 tokens
    max_caption_len = 37
    # Initialize the function that will create our vocabulary
    tokenizer = Tokenizer(filters='', split=" ", lower=False)

    # Read a document and return a string
    def load_doc(filename):
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text

    # Load all the HTML files
    X = []
    all_filenames = listdir('html/header/') #путь к html footer header
    all_filenames.sort()
    for filename in all_filenames:
        X.append(load_doc('html/header/'+filename))

    # Create the vocabulary from the html files
    tokenizer.fit_on_texts(X)

    # Add +1 to leave space for empty words
    vocab_size = len(tokenizer.word_index) + 1
    # Translate each word in text file to the matching vocabulary index
    sequences = tokenizer.texts_to_sequences(X)
    # The longest HTML file
    max_length = max(len(s) for s in sequences)


    #Load our model
    model = km.load_model('models/header/epochs-500')

    def word_for_id(integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    # generate a description for an image
    def generate_desc(model, tokenizer, photo, max_length):
        # seed the generation process
        in_text = ''
        # iterate over the whole length of the sequence
        for i in range(37): #900
            # integer encode input sequence
            sequence = tokenizer.texts_to_sequences([in_text])[0][-100:]
            # pad input
            sequence = pad_sequences([sequence], maxlen=max_length)
            # predict next wordи
            yhat = model.predict([photo,sequence], verbose=0)
            # convert probability to integer
            yhat = np.argmax(yhat)
            # map integer to word
            word = word_for_id(yhat, tokenizer)
            # stop if we cannot map the word
            if word is None:
                break
            # append as input for generating the next word
            in_text += ' ' + word
            # stop if we predict the end of the sequence
            if 'END' in word:
                break
        return in_text

    dictionary = {1: '1_header_grey', 2: '2_header_red', 3: '3_header_green', 4: '4_header_blue', 5: '5_header_yel'}
    #print(f"Start model - epochs-500 ->")

    #Для каждой картинки предсказываем текст и загружаем в файл с названием картинки

    test_image = img_to_array(load_img(path, target_size=(299, 299)))
    test_image = np.array(test_image, dtype=float)
    test_image = preprocess_input(test_image)
    test_features = IR2.predict(np.array([test_image]))
    text = generate_desc(model, tokenizer, np.array(test_features), 37)

    text_lines = text.splitlines()
    text_lines[0] = '<div' + text_lines[0][15:]
    new_text_lines = []

    for j in range(len(text_lines)):
        new_text_lines.append(text_lines[j] + '\n')


    # Определение наиболее частого цвета
    color_hex = get_popular_color_from_part(path)

    for i in range(len(new_text_lines)):
        new_text_lines[i] = re.sub('<div class=', f'<div style="background-color: {color_hex}", class=', new_text_lines[i])
        new_text_lines[i] = re.sub('<a href=', f'<a style="background-color: {color_hex}", href=', new_text_lines[i])
        new_text_lines[i] = re.sub('<(navyel|navred|navgreen|navblue|nav)', f'<nav style="background-color: {color_hex}"', new_text_lines[i])
        new_text_lines[i] = re.sub('</(navyel|navred|navgreen|navblue)', f'</nav', new_text_lines[i])



    return new_text_lines


