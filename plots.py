import inspect
import os

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


class Plotter:
    def __init__(self) -> None:
        self.save_dir = 'plots'

    def plot_mean_hist(self, dataframe: DataFrame) -> str:
        """
        Plot the distribution of mean deviations of the model.

        Save plot to the file 'mean_hist.png'. The good model should have
        hight mean deviation frequencies concentrated around 0 deviation.

        Parameters
        ----------
        dataframe : Dataframe
            Pandas Dataframe with data. Must have `mean` column.

        Returns
        -------
        str
            Path to the saved plot.
        """
        dataframe['mean'].plot.hist(bins=100)
        plt.xlabel('Mean deviation')
        return self.save_plot('mean_hist.png')

    def plot_corners_mean_bar(self, dataframe: DataFrame) -> str:
        """
        Plot the distribution of mean deviations of the model grouped by
        number of corners.

        Save plot to the file 'corners_mean_bar.png'.

        Parameters
        ----------
        dataframe : Dataframe
            Pandas Dataframe with data. Must have `mean` column.

        Returns
        -------
        str
            Path to the saved plot.
        """
        dataframe.groupby(['gt_corners'])['mean'].mean().plot.bar()
        plt.xticks(rotation='horizontal')
        plt.xlabel('Number of corners')
        plt.ylabel('Mean deviation')
        return self.save_plot('corners_mean_bar.png')

    def draw_plots(self, path: str) -> list[str]:
        """
        Draw and save plots from given json data file.

        Parameters
        ----------
        path : str
            Path to json file.

        Returns
        -------
        list
            List with paths to the saved plots.
        """
        dataframe = pd.read_json(path)
        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)
        plot_paths = []
        plot_functions = self.get_plot_functions()
        for func in plot_functions:
            plot_paths.append(func(dataframe))
            plt.show()
        return plot_paths

    def plot_ceiling_floor_mean_scatter(self, dataframe: DataFrame) -> str:
        """
        Plot diffrerence betwen floor and ceiling mean deviations.

        The closer points are to 0 the better.

        Save plot to the file 'mceiling_floor_mean_scatter.png'.

        Parameters
        ----------
        dataframe : Dataframe
            Pandas Dataframe with data. Must have `mean` column.

        Returns
        -------
        str
            Path to the saved plot.
        """
        ceiling_mean_greater = (dataframe['ceiling_mean']
                                > dataframe['floor_mean'])
        ax = dataframe[ceiling_mean_greater].plot.scatter(
            'floor_mean',
            'ceiling_mean',
            label='Ceiling deviation greter'
        )
        dataframe[ceiling_mean_greater == False].plot.scatter(
            'floor_mean',
            'ceiling_mean',
            c='red',
            ax=ax,
            label='Floor deviation greter'
        )
        plt.xlabel('Floor mean')
        plt.ylabel('Ceiling mean')
        return self.save_plot('ceiling_floor_mean_scatter.png')

    def get_plot_functions(self):
        """
        Gather all plot functions in the class.

        Plot functions must start with 'plot_'.

        Returns
        -------
        list
            list with plot functions.
        """
        names_functions = inspect.getmembers(self, inspect.ismethod)
        return [
            func for name, func in names_functions if name.startswith('plot_')
        ]

    def save_plot(self, fname: str) -> str:
        """
        Save current matplotlib figure to `save_dir` directory.

        Parameters
        ----------
        fname : str
            Save file name.

        Returns
        -------
        str
            Path to the saved figure.
        """
        save_path = os.path.join(self.save_dir, fname)
        plt.savefig(save_path)
        return save_path
