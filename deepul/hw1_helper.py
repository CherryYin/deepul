from .utils import *


# Question 1
def q1_sample_data_1():
    count = 1000
    rand = np.random.RandomState(0)
    samples = 0.4 + 0.1 * rand.randn(count)
    data = np.digitize(samples, np.linspace(0.0, 1.0, 20))
    split = int(0.8 * len(data))
    train_data, test_data = data[:split], data[split:]
    return train_data, test_data


def q1_sample_data_2():
    count = 10000
    rand = np.random.RandomState(0)
    a = 0.3 + 0.1 * rand.randn(count)
    b = 0.8 + 0.05 * rand.randn(count)
    mask = rand.rand(count) < 0.5
    samples = np.clip(a * mask + b * (1 - mask), 0.0, 1.0)
    data = np.digitize(samples, np.linspace(0.0, 1.0, 100))
    split = int(0.8 * len(data))
    train_data, test_data = data[:split], data[split:]
    return train_data, test_data


def visualize_q1_data(dset_type):
    if dset_type == 1:
        train_data, test_data = q1_sample_data_1()
    elif dset_type == 2:
        train_data, test_data = q1_sample_data_2()
    else:
        raise Exception('Invalid dset_type:', dset_type)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title('Train Data')
    ax1.hist(train_data, density=True)
    ax1.set_xlabel('x')
    ax2.set_title('Test Data')
    ax2.hist(test_data, density=True)
    print(f'Dataset {dset_type}')
    plt.show()


def q1_save_results(dset_type, part, fn):
    if dset_type == 1:
        train_data, test_data = q1_sample_data_1()
        d = 20
    elif dset_type == 2:
        train_data, test_data = q1_sample_data_2()
        d = 100
    else:
        raise Exception('Invalid dset_type:', dset_type)

    train_losses, test_losses, distribution = fn(train_data, test_data, d, dset_type)
    assert len(train_losses) == len(test_losses), 'Both train/test loss arrays should be the same length'
    assert np.allclose(np.sum(distribution), 1), f'Distribution sums to {np.sum(distribution)} != 1'

    print(f'Final Test Loss: {test_losses[-1]:.4f}')

    save_training_plot(train_losses, test_losses, f'Q1({part}) Dataset {dset_type} Train Plot',
                       f'results/q1_{part}_dset{dset_type}_train_plot.png')
    save_distribution_1d(train_data, distribution,
                         f'Q1({part}) Dataset {dset_type} Learned Distribution',
                         f'results/q1_{part}_dset{dset_type}_learned_dist.png')


# Question 2
def q2_a_sample_data(image_file, n, d):
    from PIL import Image
    from urllib.request import urlopen
    import io
    import itertools

    im = Image.open(image_file).resize((d, d)).convert('L')
    im = np.array(im).astype('float32')
    dist = im / im.sum()

    pairs = list(itertools.product(range(d), range(d)))
    idxs = np.random.choice(len(pairs), size=n, replace=True, p=dist.reshape(-1))
    samples = [pairs[i] for i in idxs]

    return dist, np.array(samples)


def visualize_q2a_data(dset_type):
    data_dir = get_data_dir(1)
    if dset_type == 1:
        n, d = 10000, 25
        true_dist, data = q2_a_sample_data(join(data_dir, 'smiley.jpg'), n, d)
    elif dset_type == 2:
        n, d = 100000, 200
        true_dist, data = q2_a_sample_data(join(data_dir, 'geoffrey-hinton.jpg'), n, d)
    else:
        raise Exception('Invalid dset_type:', dset_type)
    split = int(0.8 * len(data))
    train_data, test_data = data[:split], data[split:]

    train_dist, test_dist = np.zeros((d, d)), np.zeros((d, d))
    for i in range(len(train_data)):
        train_dist[train_data[i][0], train_data[i][1]] += 1
    train_dist /= train_dist.sum()

    for i in range(len(test_data)):
        test_dist[test_data[i][0], test_data[i][1]] += 1
    test_dist /= test_dist.sum()

    print(f'Dataset {dset_type}')
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title('Train Data')
    ax1.imshow(train_dist)
    ax1.axis('off')
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x0')

    ax2.set_title('Test Data')
    ax2.imshow(test_dist)
    ax2.axis('off')
    ax2.set_xlabel('x1')
    ax2.set_ylabel('x0')

    plt.show()


def visualize_q2b_data(dset_type):
    data_dir = get_data_dir(1)
    if dset_type == 1:
        train_data, test_data = load_pickled_data(join(data_dir, 'shapes.pkl'))
        print('Shapes Dataset')
    elif dset_type == 2:
        train_data, test_data = load_pickled_data(join(data_dir, 'mnist.pkl'))
        print('MNIST Dataset')
    else:
        raise Exception('Invalid dset type:', dset_type)

    idxs = np.random.choice(len(train_data), replace=False, size=(100,))
    images = train_data[idxs]
    show_samples(images, title='Samples From Dataset')


def q2_save_results(dset_type, part, fn):
    data_dir = get_data_dir(1)
    if part == 'a':
        if dset_type == 1:
            n, d = 10000, 25
            true_dist, data = q2_a_sample_data(join(data_dir, 'smiley.jpg'), n, d)
        elif dset_type == 2:
            n, d = 100000, 200
            true_dist, data = q2_a_sample_data(join(data_dir, 'geoffrey-hinton.jpg'), n, d)
        else:
            raise Exception('Invalid dset_type:', dset_type)
        split = int(0.8 * len(data))
        train_data, test_data = data[:split], data[split:]
    elif part == 'b':
        if dset_type == 1:
            train_data, test_data = load_pickled_data(join(data_dir, 'shapes.pkl'))
            img_shape = (20, 20)
        elif dset_type == 2:
            train_data, test_data = load_pickled_data(join(data_dir, 'mnist.pkl'))
            img_shape = (28, 28)
        else:
            raise Exception('Invalid dset type:', dset_type)
    else:
        raise Exception('Invalid part', part)

    if part == 'a':
        train_losses, test_losses, distribution = fn(train_data, test_data, d, dset_type)

        assert len(train_losses) == len(test_losses), 'Both train/test loss arrays should be the same length'
        assert np.allclose(np.sum(distribution), 1), f'Distribution sums to {np.sum(distribution)} != 1'

        print(f'Final Test Loss: {test_losses[-1]:.4f}')

        save_training_plot(train_losses, test_losses, f'Q2({part}) Dataset {dset_type} Train Plot)',
                           f'results/q2_{part}_dset{dset_type}_train_plot.png')
        save_distribution_2d(true_dist, distribution,
                             f'results/q2_{part}_dset{dset_type}_learned_dist.png')
    elif part == 'b':
        train_losses, test_losses, samples = fn(train_data, test_data, img_shape, dset_type)
        print(f'Final Test Loss: {test_losses[-1]:.4f}')
        save_training_plot(train_losses, test_losses, f'Q2({part}) Dataset {dset_type} Train Plot',
                           f'results/q2_{part}_dset{dset_type}_train_plot.png')
        show_samples(samples, f'results/q2_{part}_dset{dset_type}_samples.png')


# Question 3
def q3a_save_results(dset_type, q3_a):
    data_dir = get_data_dir(1)
    if dset_type == 1:
        train_data, test_data = load_pickled_data(join(data_dir, 'shapes.pkl'))
        img_shape = (20, 20)
    elif dset_type == 2:
        train_data, test_data = load_pickled_data(join(data_dir, 'mnist.pkl'))
        img_shape = (28, 28)

    train_losses, test_losses, samples = q3_a(train_data, test_data, img_shape, dset_type)
    print(f'Final Test Loss: {test_losses[-1]:.4f}')
    save_training_plot(train_losses, test_losses, f'Q3(a) Dataset {dset_type} Train Plot',
                       f'results/q3_a_dset{dset_type}_train_plot.png')
    save_samples(samples, f'results/q3_a_dset{dset_type}_samples.png')


def q3b_save_results(q3_b):
    data_dir = get_data_dir(1)
    train_data, test_data = load_pickled_data(join(data_dir, 'mnist_colored.pkl'))
    train_losses, test_losses, samples = q3_b(train_data, test_data, (28, 28, 3))
    print(f'final Test Loss: {test_losses[-1]:.4f}')
    save_training_plot(train_losses, test_losses, f'Q3(b) Train Plot',
                       f'results/q3_b_train_plot.png')
    save_samples(samples, f'results/q3_b_samples.png')


def q3c_save_results(q3_c):
  train_data, test_data = load_pickled_data('mnist_colored.pkl')
  img_shape = (28, 28, 3)

  train_losses, test_losses, samples = q3_c(train_data, test_data, img_shape)
  samples = samples / 3 * 255

  print(f'Final Test Loss: {test_losses[-1]:.4f}')
  save_training_plot(train_losses, test_losses, f'Q3(c) Train Plot',
                    f'results/q3_c_train_plot.png')
  save_samples(samples, f'results/q3_c_samples.png')

