from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Проверяем запрос с валидными email и password, статус код запроса и что ключ есть в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем, что список питомцев возвращается и он не пустой,
    также проверяем статус код запроса'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0

def test_add_pets_with_valid_data(name='Котякa', animal_type='cat', age='8', pet_photo='images/polosat.jpg'):
    '''Тест проверяет, что код статуса запроса 200 и список с добавленными данными не пустой. Для этого
    в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ в переменную api_key,
    проверяем статус ответа и наличие добавленных данных.
    '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet():
    '''Проверка удаления питомца'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Котяка', 'кот', '8', 'images/polosat.jpg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_put_pet_info(name='Петя', animal_type='кот', age='10'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_pets_with_valid_data_without_photo(name='Пушок', animal_type='котэ', age='12'):
    '''Проверка добавления нового питомца без фото'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_photo_at_pet(pet_photo='images/seryj.jpg'):
    '''Проверка добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("There is no my pets")


def test_add_pet_negative_age_number(name='##@$%', animal_type='cat', age='3', pet_photo='images/polosat.jpg'):
    '''Негативный сценарий. Добавление питомца со спецсимволами в поле name.
    Тест будет провален, если питомец добавится на сайт.
     '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert name not in result['name'], 'Питомец добавлен на сайт'

def test_put_pet_info(name='###########', animal_type='кот', age='1'):
    '''Негативный сценарий. Изменение name питомца на невалидные данные. Тест будет провален, если данные питомца изменятся на невалидные'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
        assert name not in result['name']
    else:
        raise Exception("There is no my pets")


def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='dog', age='7', pet_photo='images/seryj.jpg'):
    '''Проверка добавления питомца с пустым значением в переменной name
    Тест будет провален, если питомец будет добавлен на сайт с пустым значением в поле "name"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert result['name'] != '', 'Питомец добавлен на сайт'

def test_add_pet_with_four_digit_age_number(name='RAY', animal_type='dog', age='45555', pet_photo='images/polosat.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с возрастом, превышающим 2 знака в поле age.
    Тест будет провален, если питомец добавится на сайт.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 3, 'Питомец добавлен на сайт.'

def test_add_pet_with_empty_value_in_variable_name(name='Альба', animal_type='', age='11', pet_photo='images/seryj.jpg'):
    '''Проверка добавления питомца с пустым значением в переменной age
    Тест будет провален, если питомец будет добавлен на сайт с пустым значением в поле "age"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert result['animal_type'] != '', 'Питомец добавлен на сайт'


def test_add_pet_with_four_digit_age_number(name='Dirutnsaplfhwbvnljxzyfrbdhwff', animal_type='dog', age='4', pet_photo='images/polosat.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с именем, превышающим 12 знаков в поле name.
    Тест будет провален, если питомец добавится на сайт.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    quantity = result['name']

    assert len(quantity) < 13, 'Питомец добавлен на сайт.'

def test_add_pet_with_four_digit_age_number(name='Smoky', animal_type='dogfkfsfjsjhahgdhagahgsgsg', age='4', pet_photo='images/polosat.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с типом животного, превышающим 12 знаков в поле animal_type.
    Тест будет провален, если питомец добавится на сайт.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    quantity = result['animal_type']

    assert len(quantity) < 13, 'Питомец добавлен на сайт.'


def test_put_pet_info(name='Жуня', animal_type='№№№№№№№№', age='2'):
    '''Негативный сценарий. Изменение animal_type питомца на невалидные данные. Тест будет провален, если данные питомца изменятся на невалидные'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
        assert animal_type not in result['animal_type']
    else:
        raise Exception("There is no my pets")

def test_put_pet_info(name='Роберт', animal_type='кот', age='&&&&&&&'):
    '''Негативный сценарий. Изменение age питомца на невалидные данные. Тест будет провален, если данные питомца изменятся на невалидные'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
        assert age not in result['age']
    else:
        raise Exception("There is no my pets")

def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
        '''Проверяем запрос с невалидным email и с валидным password.
        Проверяем нет ли ключа в ответе'''
        status, result = pf.get_api_key(email, password)
        assert status == 403
        assert "key" not in result

