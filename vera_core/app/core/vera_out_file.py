from typing import Union

import h5py
import numpy as np

H5_ARRAY_TYPE = Union[h5py.Dataset, np.ndarray]


class VeraOutFile:
    def __init__(self, filename):
        # Keep this open for better performance
        self.f = h5py.File(filename, "r")
        self.core = VeraOutCore(self.f)
        self.core._cache_all()

        self.states = []

        self._create_states()

        self.active_state_index = 0

    def close(self):
        self.f.close()

    def _create_states(self):
        state_keys = [key for key in self.f if key.startswith("STATE_")]
        indices = [int(key.split("_")[1]) for key in state_keys]
        self.states = [VeraOutState(self.f, idx) for idx in indices]

    @property
    def active_state(self):
        return self.states[self.active_state_index]

    @property
    def active_state_index(self):
        return self._active_state_index

    @active_state_index.setter
    def active_state_index(self, index):
        if hasattr(self, "_active_state_index"):
            if self._active_state_index == index:
                return
            else:
                # Clear the cache from the active state
                self.active_state._uncache_all()

        self._active_state_index = index
        self.active_state._cache_all()


class LazyHDF5Loader:
    def __init__(self, f, path, dataset_names):
        self._f = f
        self._path = path
        self._dataset_names = dataset_names

        self._uncache_all()

    def _load_dataset(self, name):
        return self._f[f"{self._path}/{name}"]

    def _cache(self, name):
        # Set the attribute to be the loaded numpy array
        if name not in self._dataset_names:
            raise AttributeError(name)

        setattr(self, name, self._load_dataset(name)[:])

    def _uncache(self, name):
        # Set the attribute to be the h5py dataset
        if name not in self._dataset_names:
            raise AttributeError(name)

        setattr(self, name, self._load_dataset(name))

    def _cache_all(self):
        for name in self._dataset_names:
            self._cache(name)

    def _uncache_all(self):
        for name in self._dataset_names:
            self._uncache(name)


class VeraOutCore(LazyHDF5Loader):
    axial_mesh: H5_ARRAY_TYPE = None
    core_map: H5_ARRAY_TYPE = None
    core_sym: H5_ARRAY_TYPE = None
    pin_volumes: H5_ARRAY_TYPE = None

    def __init__(self, f):
        super().__init__(f, "/CORE", list(self.__annotations__))


class VeraOutState(LazyHDF5Loader):
    crit_boron: H5_ARRAY_TYPE = None
    detector_response: H5_ARRAY_TYPE = None
    exposure: H5_ARRAY_TYPE = None
    keff: H5_ARRAY_TYPE = None
    pin_cladtemps: H5_ARRAY_TYPE = None
    pin_fueltemps: H5_ARRAY_TYPE = None
    pin_moddens: H5_ARRAY_TYPE = None
    pin_modtemps: H5_ARRAY_TYPE = None
    pin_powers: H5_ARRAY_TYPE = None

    def __init__(self, f, idx):
        super().__init__(f, f"/STATE_{idx:04}", list(self.__annotations__))
        self._index = idx
