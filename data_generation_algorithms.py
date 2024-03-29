import numpy as np
from sklearn.datasets import load_digits
from scipy import ndimage


class PointGenerator():
    def __init__(self,dimension,n_points, points_shape,distribution=None, noise=False, noise_mean=0, noise_var=1):
        self.d = dimension
        self.points_shape = points_shape
        self.n_points = n_points
        self.distribution = distribution
        self.noise = noise
        self.noise_mean = noise_mean
        self.noise_var = noise_var
    
    def get_points(self):
        # Initalizing Data Matrix
        x = np.zeros((self.d,self.n_points))

        if self.distribution == "uniform":
            thetas = np.random.uniform(0, 2 * np.pi, self.n_points)

            
        elif self.distribution == "beta":
            theta = (np.random.beta(5,2, self.n_points) * (2 * np.pi + 0.2) / 0.4) - 0.2
            
        else:
            thetas = np.linspace(0,self.n_points-1, self.n_points)  * 2 * np.pi / self.n_points
        
        if self.shape == "3d_loop":
            for i in range(self.n_points):
                x[:,i] = np.array([np.sin(thetas[i]), np.cos(2 * thetas[i]), np.cos(theta[i])])
        
        elif self.shape == "3d_figure_eight":
            for i in range(self.n_points):
                x[:,i] = np.array([np.sin(2 * thetas[i]), np.cos(thetas[i]), np.cos(thetas[i]) + np.cos((thetas[i]/2) - np.pi / 4) ** 2])

        elif self.shape == "unit_circle":
            # Generate Two Random Orthonormal Vectors
            u = np.random.standard_normal(self.d)
            u /= np.linalg.norm(u)
            v = np.random.standard_normal(self.d)
            v -= v.dot(u) * u
            v /= np.linalg.norm(v)
            
            for i in range(self.n_points):
                x[:,i] = np.cos(thetas[i]) * u + np.sin(thetas[i]) * v

        elif self.shape == "unit_sphere":
            if self.distribution == "uniform":
                for i in range(self.n_points):
                    point = np.random.standard_normal(self.d)
                    x[:,i] = point / np.linalg.norm(point)

            elif self.distribution == "beta":
                for i in range(self.n_points):
                    point = (np.random.beta(5,2,self.n_dimension) * (2 * np.pi + 0.2) / 0.4) - 0.2
                    x[:,i] = point / np.linalg.norm(point)
        else:
            print(f"Shape {self.shape} is not valid")
            return

        # Adding Noise
        if self.noise:
            x += np.random.normal(self.noise_mean, self.noise_var, size=(self.d,self.n_points))

        return x
    


def generate_3d_loop(n_points,distribution=None, noise=False, noise_mean=0, noise_var=1):

    # Initalizing Data Matrix
    x = np.zeros((3,n_points))

    # Specify Distribution to Draw Data Points
    if distribution=="uniform":
        for i in range(n_points):
            theta = np.random.uniform(0, 2 * np.pi)
            x[:,i] = np.array([np.sin(theta), np.cos(2 * theta), np.cos(theta)])
      
    elif distribution=="beta":
        for i in range(n_points):
            theta = (np.random.beta(5,2) * (2 * np.pi + 0.2) / 0.4) - 0.2
            x[:,i] = np.array([np.sin(theta), np.cos(2 * theta), np.cos(theta)])
   
    else:
        for i in range(n_points):
            theta = i * 2 * np.pi / n_points
            x[:,i] = np.array([np.sin(theta), np.cos(2 * theta), np.cos(theta)])
          
    # Adding Noise
    if noise:
        x += np.random.normal(noise_mean, noise_var, size=(3,n_points))

    return x

def generate_3d_figure_eight(n_points,distribution=None, noise=False, noise_mean=0, noise_var=1):

    # Initalizing Data Matrix
    x = np.zeros((3,n_points))

    # Specify Distribution to Draw Data Points
    if distribution=="uniform":
        for i in range(n_points):
            theta = np.random.uniform(0, 2 * np.pi)
            x[:,i] = np.array([np.sin(2 * theta), np.cos(theta), np.cos(theta) + np.cos((theta/2) - np.pi / 4) ** 2])
      
    elif distribution=="beta":
        for i in range(n_points):
            theta = (np.random.beta(5,2) * (2 * np.pi + 0.2) / 0.4) - 0.2
            x[:,i] = np.array([np.sin(2 * theta), np.cos(theta), np.cos(theta) + np.cos((theta/2) - np.pi / 4) ** 2])   
    else:
        for i in range(n_points):
            theta = i * 2 * np.pi / n_points
            x[:,i] = np.array([np.sin(2 * theta), np.cos(theta), np.cos(theta) + np.cos((theta/2) - np.pi / 4) ** 2])          
    # Adding Noise
    if noise:
        x += np.random.normal(noise_mean, noise_var, size=(3,n_points))

    return x

def generate_unit_circle_points(n_points, n_dimension, distribution=None, 
                                noise=False, noise_mean=0, noise_var=1):

    # Initalizing Data Matrix
    x = np.zeros((n_dimension,n_points))

    # Generate Two Random Orthonormal Vectors
    u = np.random.standard_normal(n_dimension)
    u /= np.linalg.norm(u)
    v = np.random.standard_normal(n_dimension)
    v -= v.dot(u) * u
    v /= np.linalg.norm(v)


    # Specify Distribution to Draw Data Points
    if distribution=="uniform":
        for i in range(n_points):
            theta = np.random.uniform(0, 2 * np.pi)
            x[:,i] = np.cos(theta) * u + np.sin(theta) * v
      
    elif distribution=="beta":
        for i in range(n_points):
            theta = (np.random.beta(5,2) * (2 * np.pi + 0.2) / 0.4) - 0.2
            x[:,i] = np.cos(theta) * u + np.sin(theta) * v
   
    else:
        for i in range(n_points):
            theta = i * 2 * np.pi / n_points
            x[:,i] = np.cos(theta) * u + np.sin(theta) * v
          
    # Adding Noise
    if noise:
        x += np.random.normal(noise_mean, noise_var, size=(n_dimension,n_points))

    return x


def generate_unit_sphere_points(n_points, n_dimension, distribution="uniform", 
                                noise=False, noise_mean=0, noise_var=1):

    # Initializing Data Matrix
    x = np.zeros((n_dimension,n_points))


    # Specify Distribution to Draw Data Points
    if distribution == "uniform":
        for i in range(n_points):
            point = np.random.standard_normal(n_dimension)
            x[:,i] = point / np.linalg.norm(point)

    elif distribution == "beta":
        for i in range(n_points):
            point = (np.random.beta(5,2,n_dimension) * (2 * np.pi + 0.2) / 0.4) - 0.2
            x[:,i] = point / np.linalg.norm(point)
    else:
        print("Please Select \"Uniform\" or \"Beta\" Distrubtion")
         
    #Adding Noise
    if noise:
        x += np.random.normal(noise_mean, noise_var, size=(n_dimension,n_points))

    return x


def generate_rotating_img_points(img_number, n_images, padding, 
                                  noise=False, noise_mean=0, noise_var=1):

    # Loading MNIST Dataset via Sklearn
    digits = load_digits()

    # Chooisng a Particular Image to Generate Points
    img = digits.images[img_number]

    # Initializing Array to Store Images
    size=(n_images,(8 + 2 * padding)**2)

    # Generating Data Matrix
    x = np.zeros(size)

    # Rotating and Flattening Image and then Adding to Data Matrix
    for i in range(n_images):
        theta = i * 360 / n_images
        img_padded = np.pad(img, padding)
        img_rotate = ndimage.rotate(img_padded, theta, reshape=False)
        img_flat = img_rotate.flatten()

        x[i,:] = img_flat

    # Adding Noise
    if noise:
        x += np.random.normal(noise_mean, noise_var, size=size)

    return x


def generate_3d_intersecting_figure_eight(n_points,distribution=None, noise=False, noise_mean=0, noise_var=1):

    # Initalizing Data Matrix
    x = np.zeros((3,n_points))

    # Specify Distribution to Draw Data Points
    if distribution=="uniform":
        for i in range(n_points):
            theta = np.random.uniform(0, 2 * np.pi)
            x[:,i] = np.array([np.sin(theta), np.cos(theta) * np.sin(theta), np.cos(2 * theta)])
      
    elif distribution=="beta":
        for i in range(n_points):
            theta = (np.random.beta(5,2) * (2 * np.pi + 0.2) / 0.4) - 0.2
            x[:,i] = np.array([np.sin(theta), np.cos(theta) * np.sin(theta), np.cos(2 * theta)])
    else:
        for i in range(n_points):
            theta = i * 2 * np.pi / n_points
            x[:,i] = np.array([np.sin(theta), np.cos(theta) * np.sin(theta), np.cos(2 * theta)])
    # Adding Noise
    if noise:
        x += np.random.normal(noise_mean, noise_var, size=(3,n_points))

    return x

