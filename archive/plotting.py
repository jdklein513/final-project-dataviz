##### Import Libraries -----

# data manipulation
import numpy as np
import pandas as pd 

# plotting
import seaborn as sns
import matplotlib.pyplot as plt
from plotnine import *
from matplotlib import gridspec
import plotly.graph_objects as go
from math import pi
from IPython.display import Markdown as md

# pybaseball
from pybaseball import playerid_reverse_lookup
import pybaseball as pyb


##### Define Functions -----

'''
Define a function for loading in dataset
'''
def load_data(in_path, name):
    df = pd.read_csv(in_path)
    return df


'''
Define a function to filter the original statcast data to the desired scope
'''
def statcast_df_filter(data,
                       pitcher_name_filter,
                       pitch_name_filter,
                       stand_filter,
                       batter_name_filter, 
                       count_filter,
                       count_advantage_filter,
                       outs_when_up_filter,
                       inning_filter,
                       runners_on_base_filter,
                       run_differential_filter):
    
    # filter pitcher name
    statcast_df_filtered = data[data['pitcher_name'] == pitcher_name_filter]
    
    # filter pitch name
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['pitch_name'].isin(pitch_name_filter)]
    
    # filter batter stance
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['stand'].isin(stand_filter)]
    
    # filter batter name
    if batter_name_filter != 'All':
        statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['batter_name'] == batter_name_filter]
        
    # filter count
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['count'].isin(count_filter)]
    
    # filter count advantage
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['count_advantage'].isin(count_advantage_filter)]
    
    # filter outs
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['outs_when_up'].isin(outs_when_up_filter)]
    
    # filter inning
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['inning'].isin(inning_filter)]
    
    # filter runners on base
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['runners_on_base'].isin(runners_on_base_filter)]
    
    # filter run differential
    statcast_df_filtered = statcast_df_filtered[(statcast_df_filtered['run_differential'] >= run_differential_filter[0]) &
                                                (statcast_df_filtered['run_differential'] <= run_differential_filter[1])]
    
    return statcast_df_filtered


'''
Define a function to filter the original statcast data to the desired scope.
Does not filter on pitcher.
'''
def statcast_df_non_pitcher_filter(data,
                                   pitcher_name_filter,
                                   pitch_name_filter,
                                   stand_filter,
                                   batter_name_filter, 
                                   count_filter,
                                   count_advantage_filter,
                                   outs_when_up_filter,
                                   inning_filter,
                                   runners_on_base_filter,
                                   run_differential_filter):
    
    # filter pitch name
    statcast_df_filtered = data[data['pitch_name'].isin(pitch_name_filter)]
    
    # filter batter stance
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['stand'].isin(stand_filter)]
    
    # filter batter name
    if batter_name_filter != 'All':
        statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['batter_name'] == batter_name_filter]
        
    # filter count
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['count'].isin(count_filter)]
    
    # filter count advantage
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['count_advantage'].isin(count_advantage_filter)]
    
    # filter outs
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['outs_when_up'].isin(outs_when_up_filter)]
    
    # filter inning
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['inning'].isin(inning_filter)]
    
    # filter runners on base
    statcast_df_filtered = statcast_df_filtered[statcast_df_filtered['runners_on_base'].isin(runners_on_base_filter)]
    
    # filter run differential
    statcast_df_filtered = statcast_df_filtered[(statcast_df_filtered['run_differential'] >= run_differential_filter[0]) &
                                                (statcast_df_filtered['run_differential'] <= run_differential_filter[1])]
    
    return statcast_df_filtered


'''
Define a function to print number of pitches given dashboard filters
'''
def number_of_pitches(data,
                      pitcher_name_filter,
                      pitch_name_filter,
                      stand_filter,
                      batter_name_filter, 
                      count_filter,
                      count_advantage_filter,
                      outs_when_up_filter,
                      inning_filter,
                      runners_on_base_filter,
                      run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)
    
    num_observations = len(statcast_df_filtered)
    
    display(md("**<font size='8'>{}</font>**".format(num_observations)))
    

'''
Define a function to print bar plot of pitch selection percents given dashboard filters
'''
def pitch_selection_bar(data,
                        pitcher_name_filter,
                        pitch_name_filter,
                        stand_filter,
                        batter_name_filter, 
                        count_filter,
                        count_advantage_filter,
                        outs_when_up_filter,
                        inning_filter,
                        runners_on_base_filter,
                        run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)
    
    # create a dataframe with counts and relative frequency of pitch name
    temp_df1 = pd.DataFrame(statcast_df_filtered.groupby(['pitch_name'])['pitch_name'].count())
    temp_df1 = pd.DataFrame(temp_df1['pitch_name'] / temp_df1.groupby([True]*len(temp_df1))['pitch_name'].transform('sum')).add_suffix('_percent').reset_index()

    # determine order and create a categorical type of pitch name
    pitch_name_list = temp_df1.sort_values(by = 'pitch_name_percent').pitch_name.tolist()
    pitch_name_cat = pd.Categorical(temp_df1['pitch_name'], categories = pitch_name_list)

    # assign category to a new column
    temp_df1 = temp_df1.assign(pitch_name_cat = pitch_name_cat)

    # plot a bar chart of the relative frequency of pitch selection
    (ggplot(temp_df1) +
      aes(x = 'pitch_name_cat', y = 'pitch_name_percent', fill = 'pitch_name') +
      geom_bar(size = 20, stat = 'identity') +
      coord_flip() +
      geom_text(aes(label = 'pitch_name_percent*100'), format_string = '{:.1f}%', position = position_stack(vjust = 0.5)) +
      scale_y_continuous(labels = lambda l: ["%d%%" % (v * 100) for v in l]) +
      labs(x = "Pitch Type", y = "% of Pitches", title = "Pitch Selection Breakdown", fill = "")  +
      theme_minimal() +
      theme(legend_position = "none",
            panel_grid_major = element_blank(),
	    panel_grid_minor = element_blank(),
            axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
            axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
            figure_size = (8, 5))).draw();
    
    
'''
Define a function to plot pitch frequency by count given dashboard filters
'''
def pitch_count_bar(data,
                    pitcher_name_filter,
                    pitch_name_filter,
                    stand_filter,
                    batter_name_filter, 
                    count_filter,
                    count_advantage_filter,
                    outs_when_up_filter,
                    inning_filter,
                    runners_on_base_filter,
                    run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)

    # create a dataframe with counts and relative frequency of count
    temp_df1 = pd.DataFrame(statcast_df_filtered.groupby(['count'])['count'].count())
    temp_df1 = pd.DataFrame(temp_df1['count'] / temp_df1.groupby([True]*len(temp_df1))['count'].transform('sum')).add_suffix('_percent').reset_index()

    # determine order and create a categorical type of count
    count_list = temp_df1.sort_values(by = 'count_percent')['count'].tolist()
    count_cat = pd.Categorical(temp_df1['count'], categories = count_list)

    # assign category to a new column
    temp_df1 = temp_df1.assign(count_cat = count_cat)

    # plot a bar chart of the relative frequency of count
    (ggplot(temp_df1) +
      aes(x = 'count_cat', y = 'count_percent') +
      geom_bar(size = 20, stat = 'identity') +
      coord_flip() +
      geom_text(aes(label = 'count_percent*100'), format_string = '{:.1f}%', position = position_stack(vjust = 0.5)) +
      scale_y_continuous(labels=lambda l: ["%d%%" % (v * 100) for v in l]) +
      labs(x = "Count", y = "% of Pitches", title = "Pitch Count Breakdown", fill = "")  +
      theme_minimal() +
      theme(legend_position = "none",
            panel_grid_major = element_blank(),
            panel_grid_minor = element_blank(),
            axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
            axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
            figure_size = (8, 5))).draw();
    
    
'''
Define a function to plot pitch type percent by count given dashboard filters
'''    
def pitch_count_stacked_bar(data,
                            pitcher_name_filter,
                            pitch_name_filter,
                            stand_filter,
                            batter_name_filter, 
                            count_filter,
                            count_advantage_filter,
                            outs_when_up_filter,
                            inning_filter,
                            runners_on_base_filter,
                            run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)
    
    # create a dataframe with counts and relative frequency of count
    temp_df1 = pd.DataFrame(statcast_df_filtered.groupby(['count'])['count'].count())
    temp_df1 = pd.DataFrame(temp_df1['count'] / temp_df1.groupby([True]*len(temp_df1))['count'].transform('sum')).add_suffix('_percent').reset_index()

    # determine order and create a categorical type of count
    count_list = temp_df1.sort_values(by = 'count_percent')['count'].tolist()
    count_cat = pd.Categorical(temp_df1['count'], categories = count_list)

    # assign category to a new column
    temp_df1 = temp_df1.assign(count_cat = count_cat)

    # create a dataframe with counts and relative frequency of count and pitch name
    temp_df2 = pd.DataFrame(statcast_df_filtered.groupby(['count', 'pitch_name'])['count'].count()).add_suffix('_group').reset_index()
    temp_df3 = pd.DataFrame(temp_df2['count_group'] / temp_df2.groupby('count')['count_group'].transform('sum')).add_suffix('_percent')
    temp_df4 = pd.concat([temp_df2.reset_index(drop = True), temp_df3], axis = 1)

    # determine order and create a categorical type of count
    count_list = temp_df1.sort_values(by = 'count_percent')['count'].tolist()
    count_cat = pd.Categorical(temp_df4['count'], categories = count_list)

    # assign category to a new column
    temp_df4 = temp_df4.assign(count_cat = count_cat)

    # plot a bar chart of the relative frequency of pitch selection by count
    (ggplot(temp_df4) +
      aes(x = 'count_cat', y = 'count_group_percent', fill = 'pitch_name') +
      geom_bar(size = 20, stat = 'identity', position = "stack") +
      coord_flip() +
      geom_text(aes(label = 'count_group_percent*100'), format_string = '{:.1f}%', position = position_stack(vjust = 0.5)) +
      scale_y_continuous(labels = lambda l: ["%d%%" % (v * 100) for v in l]) +
      labs(x = "Count", y = "% of Pitches", title = "Pitch Count Breakdown", fill = "Pitch Type") +
      theme_minimal() +
      theme(panel_grid_major = element_blank(),
            panel_grid_minor = element_blank(),
            axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
            axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
            figure_size = (8, 5))).draw();
    
    
'''
Define a function to plot pitch type percent by count advantage given dashboard filters
'''
def pitch_count_advantage_stacked_bar(data,
                                      pitcher_name_filter,
                                      pitch_name_filter,
                                      stand_filter,
                                      batter_name_filter, 
                                      count_filter,
                                      count_advantage_filter,
                                      outs_when_up_filter,
                                      inning_filter,
                                      runners_on_base_filter,
                                      run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)

    # create a dataframe with counts and relative frequency
    temp_df2 = pd.DataFrame(statcast_df_filtered.groupby(['count_advantage', 'pitch_name'])['count_advantage'].count()).add_suffix('_group').reset_index()
    temp_df3 = pd.DataFrame(temp_df2['count_advantage_group'] / temp_df2.groupby('count_advantage')['count_advantage_group'].transform('sum')).add_suffix('_percent')
    temp_df4 = pd.concat([temp_df2.reset_index(drop=True), temp_df3], axis = 1)

    # plot a bar chart of the relative frequency of pitch selection by count
    (ggplot(temp_df4) +
      aes(x = 'count_advantage', y = 'count_advantage_group_percent', fill = 'pitch_name') +
      geom_bar(size = 20, stat = 'identity', position = "stack") +
      coord_flip() +
      geom_text(aes(label = 'count_advantage_group_percent*100'), format_string = '{:.1f}%', position = position_stack(vjust = 0.5)) +
      scale_y_continuous(labels = lambda l: ["%d%%" % (v * 100) for v in l]) +
      labs(x = "Pitcher\nCount\nAdvantage", y = "% of Pitches", title = "Pitch Count Breakdown", fill = "Pitch Type") +
      theme_minimal() +
      theme(panel_grid_major = element_blank(),
            panel_grid_minor = element_blank(),
            axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
            axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
            figure_size = (8, 2))).draw();
    

'''
Define a function to plot pitch location broken down by selection given dashboard filters
'''
def plot_pitch_location(data,
                        pitcher_name_filter,
                        pitch_name_filter,
                        stand_filter,
                        batter_name_filter, 
                        count_filter,
                        count_advantage_filter,
                        outs_when_up_filter,
                        inning_filter,
                        runners_on_base_filter,
                        run_differential_filter,
                        breakdown_var_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)

    # initialise a list which will store the breakdown plots
    plots = list()

    # initialize the breakdown variable
    if breakdown_var_filter == 'none':
        breakdown = statcast_df_filtered['pitcher_name']
    else:
        breakdown = statcast_df_filtered[breakdown_var_filter]

    # get breakdown variable categories
    categories = breakdown.value_counts().index.tolist()

    # create subplot for each level of category in breakdown variable
    for j, i in enumerate(categories):
        
        dat = statcast_df_filtered[breakdown == i]
        
        # if number of pitches is greater than 50
        # plot 2d density of pitch location
        if len(dat) >= 50:
            
            if j == 0:
                leg_pos = 'bottom'
            else:
                leg_pos = 'none'
            
            p1 = (ggplot(dat) +
                    aes(x = 'plate_x*-1', y = 'plate_z_norm') +
                    stat_density_2d(aes(fill = 'stat(..level..)'), geom = "polygon", levels = 30) +
                    geom_rect(aes(xmin = -0.83, xmax = 0.83, ymin = 1.574895560522476, ymax = 3.394016229859721), alpha = 0, color = 'white') +
                    coord_cartesian(ylim = [1, 4], xlim = [-1.66, 1.66]) +
                    labs(title = i, fill='           Density') +
                    theme_minimal() +
                    theme(legend_position = leg_pos,
                          panel_background = element_rect(fill = '#440154FF', color = '#440154FF'),
                          panel_grid_major = element_blank(),
                          panel_grid_minor = element_blank(),
                          axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
                          axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
                          axis_ticks = element_blank(),
                          axis_text = element_blank(),
                          figure_size = (10, 5)))
        else:
            p1 = (ggplot(dat) +
                    aes(x = 'plate_x*-1', y = 'plate_z_norm') +
                    geom_point(alpha=.3) +
                    geom_rect(aes(xmin = -0.83, xmax = 0.83, ymin = 1.574895560522476, ymax = 3.394016229859721), alpha = 0, color = 'grey') +
                    coord_cartesian(ylim = [1, 4], xlim = [-1.66, 1.66]) +
                    labs(title = i) +
                    theme_minimal() +
                    theme(legend_position = 'none',
                          panel_grid_major = element_blank(),
                          panel_grid_minor = element_blank(),
                          axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
                          axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
                          axis_ticks = element_blank(),
                          axis_text = element_blank(),
                          figure_size = (10, 5)))

        # append plot to list
        plots.append(p1)

    # create empty figure for subplots to be added
    fig = (ggplot() + 
              geom_blank(data = statcast_df_filtered) + 
              theme_void() + 
              theme(figure_size = (5*len(categories), 5))).draw()

    # create grid specification
    gs = gridspec.GridSpec(1, len(categories))

    # initialise a blank list for the subplots
    ax = list()

    # for each level of the category assign subplot to grid
    for i in range(len(categories)):
        ax.append(fig.add_subplot(gs[0, i]))
        ax[i].set_title(categories[i])

        # add subplot to figure
        _ = plots[i]._draw_using_figure(fig, [ax[i]])

    # show figure
    fig.show()
    
    
'''
Define a function to plot scatterplot of pitch movement by pitch type given dashboard filters
'''
def pitch_movement_scatter(data,
                           pitcher_name_filter,
                           pitch_name_filter,
                           stand_filter,
                           batter_name_filter, 
                           count_filter,
                           count_advantage_filter,
                           outs_when_up_filter,
                           inning_filter,
                           runners_on_base_filter,
                           run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)

    # plot the pitch movement by pitch name
    (ggplot(statcast_df_filtered) +
       aes(x = 'pfx_x*-12', y = 'pfx_z*12', color = 'pitch_name') +
       geom_point() +
       scale_x_continuous(limits = [-36, 36], breaks = list(range(-36, 48, 12))) +
       labs(x = "Horizontal Movement", y = "Vertical \nMovement", title = "Pitch Movement (inches) by Pitch Type", color = "Pitch Type") +
       theme_minimal() +
       theme(panel_grid_major = element_blank(),
             panel_grid_minor = element_blank(),
             axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
             axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
             figure_size = (5, 5))).draw();
    

'''
Define a function to plot scatterplot of pitch release point by pitch type given dashboard filters
'''
def pitch_release_scatter(data,
                          pitcher_name_filter,
                          pitch_name_filter,
                          stand_filter,
                          batter_name_filter, 
                          count_filter,
                          count_advantage_filter,
                          outs_when_up_filter,
                          inning_filter,
                          runners_on_base_filter,
                          run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)

    # plot the pitch release position by pitch type
    (ggplot(statcast_df_filtered) +
       aes(x = 'release_pos_x', y = 'release_pos_z', color = 'pitch_name') +
       geom_point() +
       scale_x_continuous(limits = [-5, 5]) +
       scale_y_continuous(limits = [0, 7]) +
       labs(x = "Horizontal Release Point", y = "Vertical \nRelease\nPoint", title = "Pitch Release Point (feet) by Pitch Type", color = "Pitch Type") +
       theme_minimal() +
       theme(panel_grid_major = element_blank(),
             panel_grid_minor = element_blank(),
             axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
             axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
             figure_size = (5, 5))).draw();
    

'''
Define a function to plot bar plot of pitch event results given dashboard filters
'''
def pitch_result_bar(data,
                     pitcher_name_filter,
                     pitch_name_filter,
                     stand_filter,
                     batter_name_filter, 
                     count_filter,
                     count_advantage_filter,
                     outs_when_up_filter,
                     inning_filter,
                     runners_on_base_filter,
                     run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)

    # create a dataframe with counts and relative frequency of event
    temp_df1 = pd.DataFrame(statcast_df_filtered.groupby(['events'])['events'].count())
    temp_df1 = pd.DataFrame(temp_df1['events'] / temp_df1.groupby([True]*len(temp_df1))['events'].transform('sum')).add_suffix('_percent').reset_index()

    # order and create a categorical variable of event
    events_list = temp_df1.sort_values(by = 'events_percent').events.tolist()
    events_cat = pd.Categorical(temp_df1['events'], categories = events_list)

    # assign category to a new column
    temp_df1 = temp_df1.assign(events_cat = events_cat)

    # plot a bar chart of the relative frequency of at bat event
    (ggplot(temp_df1) +
      aes(x = 'events_cat', y = 'events_percent', fill = 'events') +
      geom_bar(size = 20, stat = 'identity') +
      coord_flip() +
      geom_text(aes(label = 'events_percent*100'), format_string = '{:.1f}%', position=position_stack(vjust = 0.5)) +
      scale_y_continuous(labels = lambda l: ["%d%%" % (v * 100) for v in l]) +
      labs(x = "Result Type", y = "% of At-bats", title = "Results Breakdown", fill = "")  +
      theme_minimal() +
      theme(legend_position = "none",
            panel_grid_major = element_blank(),
            panel_grid_minor = element_blank(),
            axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
            axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
            figure_size = (8, 5))).draw();
    

'''
Define a function to plot bar plot of batted ball type given dashboard filters
'''
def pitch_bb_type_bar(data,
                      pitcher_name_filter,
                      pitch_name_filter,
                      stand_filter,
                      batter_name_filter, 
                      count_filter,
                      count_advantage_filter,
                      outs_when_up_filter,
                      inning_filter,
                      runners_on_base_filter,
                      run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)
    
    # create a dataframe with counts and relative frequency of batted ball type
    temp_df1 = pd.DataFrame(statcast_df_filtered[statcast_df_filtered['batted_ball_type'] != "nan"].groupby(['batted_ball_type'])['batted_ball_type'].count())
    temp_df1 = pd.DataFrame(temp_df1['batted_ball_type'] / temp_df1.groupby([True]*len(temp_df1))['batted_ball_type'].transform('sum')).add_suffix('_percent').reset_index()

    # order and create a categorical variable of batted ball type
    batted_ball_type_list = temp_df1.sort_values(by = 'batted_ball_type_percent').batted_ball_type.tolist()
    batted_ball_type_cat = pd.Categorical(temp_df1['batted_ball_type'], categories = batted_ball_type_list)

    # assign category to a new column
    temp_df1 = temp_df1.assign(batted_ball_type_cat = batted_ball_type_cat)

    # plot a bar chart of the relative frequency of batted ball type
    (ggplot(temp_df1) +
      aes(x = 'batted_ball_type_cat', y = 'batted_ball_type_percent', fill = 'batted_ball_type') +
      geom_bar(size = 20, stat = 'identity') +
      coord_flip() +
      geom_text(aes(label = 'batted_ball_type_percent*100'), format_string = '{:.1f}%', position = position_stack(vjust = 0.5)) +
      scale_y_continuous(labels = lambda l: ["%d%%" % (v * 100) for v in l]) +
      labs(x = "Result Type", y = "% of At-bats", title = "Results Breakdown", fill = "")  +
      theme_minimal() +
      theme(legend_position = "none",
            panel_grid_major = element_blank(),
            panel_grid_minor = element_blank(),
            axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
            axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
            figure_size=(8, 5))).draw();
    
    
'''
Define a function to plot scatterplot of batted balls given dashboard filters
'''
def pitch_bb_location(data,
                      pitcher_name_filter,
                      pitch_name_filter,
                      stand_filter,
                      batter_name_filter, 
                      count_filter,
                      count_advantage_filter,
                      outs_when_up_filter,
                      inning_filter,
                      runners_on_base_filter,
                      run_differential_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)
    
    # plot a scatterplot of batted ball location
    pyb.spraychart(statcast_df_filtered, 'dodgers', title = 'Batted Ball Spray Chart', size = 50)
    

'''
Define a function to plot pitcher performance by times through order (tto) given dashboard filters
'''
def pitcher_tto_line(data,
                     pitcher_name_filter,
                     pitch_name_filter,
                     stand_filter,
                     batter_name_filter, 
                     count_filter,
                     count_advantage_filter,
                     outs_when_up_filter,
                     inning_filter,
                     runners_on_base_filter,
                     run_differential_filter,
                     breakdown_tto_var_filter):
    
    # filter data
    statcast_df_filtered = statcast_df_filter(data,
                                              pitcher_name_filter,
                                              pitch_name_filter,
                                              stand_filter,
                                              batter_name_filter, 
                                              count_filter,
                                              count_advantage_filter,
                                              outs_when_up_filter,
                                              inning_filter,
                                              runners_on_base_filter,
                                              run_differential_filter)
    
    # group the data frame by pitcher and times through order and calculate a number of stats from each group
    tto_summary = statcast_df_filtered.groupby(
        ['pitcher_name', 'tto']
    ).agg(
        {
            'game_pk':'count',
            'strike_ind': "mean",
            'whiff_ind': "mean",
            'woba_value':"mean",
            'launch_speed':'mean',
            'release_spin_rate':'mean'
        }
    ).reset_index()

    # reformat output
    tto_summary['Strike %'] = round(tto_summary['strike_ind']*100, 1)
    tto_summary['Whiff %'] = round(tto_summary['whiff_ind']*100, 1)
    tto_summary['wOBA'] = tto_summary['woba_value']
    tto_summary['Exit Velocity'] = tto_summary['launch_speed']
    tto_summary['Spin Rate'] = tto_summary['release_spin_rate']
    
    # plot the statistic summary by times through order
    (ggplot(tto_summary) +
      aes(x = 'tto', y = breakdown_tto_var_filter) +
      geom_point(stat = 'identity') +
      geom_line(stat = 'identity') +
      geom_text(aes(label = breakdown_tto_var_filter), format_string = '{:.2f}', va = "bottom", ha = "left") +
      labs(x = "Times through order", title = "Statistics by Times Through Order")  +
      theme_minimal() +
      scale_x_continuous(limits = [1, 4.2]) +
      theme(legend_position = "none",
            panel_grid_major = element_blank(),
            panel_grid_minor = element_blank(),
            axis_title_y = element_text(angle = 0, margin = dict([('r', 40)])),
            axis_title_x = element_text(angle = 0, margin = dict([('t', 15)])),
            figure_size = (8, 5))).draw();
    

'''
Define a function to print table of pitcher statistics vs. MLB and
plot radar chart with MLB pitcher percentiles given dashboard filters
'''
def pitcher_compare(data,
                    pitcher_name_filter,
                    pitch_name_filter,
                    stand_filter,
                    batter_name_filter, 
                    count_filter,
                    count_advantage_filter,
                    outs_when_up_filter,
                    inning_filter,
                    runners_on_base_filter,
                    run_differential_filter):
    
    # filter data to all mlb pitchers
    statcast_df_non_pitcher_filtered = statcast_df_non_pitcher_filter(data,
                                                                      pitcher_name_filter,
                                                                      pitch_name_filter,
                                                                      stand_filter,
                                                                      batter_name_filter, 
                                                                      count_filter,
                                                                      count_advantage_filter,
                                                                      outs_when_up_filter,
                                                                      inning_filter,
                                                                      runners_on_base_filter,
                                                                      run_differential_filter)
    
    # group the data frame by pitcher and calculate a number of stats from each group
    statcast_pitcher_summary = statcast_df_non_pitcher_filtered.groupby(
        ['pitcher_name']
    ).agg(
        {
            'strike_ind': "mean",
            'whiff_ind': "mean",
            'woba_value':"mean",
            'launch_speed':'mean',
            'release_spin_rate':'mean'
        }
    ).reset_index()
    
    # calculate pitcher percentile for all statistics
    statcast_pitcher_summary['strike_ind_pct'] = statcast_pitcher_summary.strike_ind.rank(pct = True)*100
    statcast_pitcher_summary['whiff_ind_pct'] = statcast_pitcher_summary.whiff_ind.rank(pct = True)*100
    statcast_pitcher_summary['woba_value_pct'] = (1 - statcast_pitcher_summary.woba_value.rank(pct = True))*100
    statcast_pitcher_summary['launch_speed_pct'] = (1 - statcast_pitcher_summary.launch_speed.rank(pct = True))*100
    statcast_pitcher_summary['release_spin_rate_pct'] = statcast_pitcher_summary.release_spin_rate.rank(pct = True)*100
    
    # filter to pitcher of interest
    statcast_pitcher_summary_filtered = statcast_pitcher_summary[statcast_pitcher_summary['pitcher_name'] == pitcher_name_filter]
    
    # group all other pitchers outside of pitcher of interest to same group
    statcast_df_non_pitcher_filtered['pitcher_ind'] = np.where(statcast_df_non_pitcher_filtered['pitcher_name'] == pitcher_name_filter, pitcher_name_filter, 'Rest of MLB')

    # group the data frame by pitcher category and extract a number of stats from each group
    compare_df = statcast_df_non_pitcher_filtered.groupby(
        ['pitcher_ind']
    ).agg(
        {
            'strike_ind': "mean",
            'whiff_ind': "mean",
            'woba_value':"mean",
            'launch_speed':'mean',
            'release_spin_rate':'mean'
        }
    ).reset_index()
    
    # reformat output
    compare_df['strike_ind'] = round(compare_df['strike_ind']*100, 1).astype(str)
    compare_df['whiff_ind'] = round(compare_df['whiff_ind']*100, 1).astype(str)
    compare_df['woba_value'] = round(compare_df['woba_value'], 3).astype(str)
    compare_df['launch_speed'] = round(compare_df['launch_speed'], 1).astype(str)
    compare_df['release_spin_rate'] = round(compare_df['release_spin_rate'], 1).astype(str)
    
    # set the column names of the clean table output
    compare_df.columns = [" ", 'Strike %', 'Whiff %', 'wOBA', 'Avg. Exit Velocity', 'Avg. Spin Rate']
    
    # display statistics table
    display(compare_df)
    
    # set variables to select from summary data
    categories=['strike_ind_pct', 'whiff_ind_pct', 'woba_value_pct', 'launch_speed_pct', 'release_spin_rate_pct']
    
    # set clean names of variables for labelling
    categories_clean=['Strike %', 'Whiff %', 'wOBA', 'Avg. Exit Velocity', 'Avg. Spin Rate']
    
    # get number of categories
    N = len(categories)

    # plot the values - need to set the last value to the first value to close loop
    values = np.array(statcast_pitcher_summary_filtered[categories])[0].tolist()
    values += values[:1]

    # set angles for each statistic in radar chart
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # initialise the radar plot size
    plt.figure(figsize = (8, 8), facecolor='white')
    
    # initialise the sub plot
    ax = plt.subplot(111, polar = True)

    # set x ticks
    plt.xticks(angles[:-1], categories_clean, color = 'grey', size = 15)

    # set y labels
    ax.set_rlabel_position(30)
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color = "grey", size = 15)
    plt.ylim(0,100)

    # plot data
    ax.plot(angles, values, linewidth = 1, linestyle = 'solid')

    # fill area
    ax.fill(angles, values, 'b', alpha = 0.2)
    
    # set plot title
    ax.set_title("Pitcher Performance MLB Percentiles", size = 15)
    
    # set spin to invisible
    ax.spines['polar'].set_visible(False)
    
    # print space
    print("")
    
    # show plot
    plt.show()