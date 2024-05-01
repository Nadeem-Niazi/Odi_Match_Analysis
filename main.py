import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns

## Page Layout 
st.set_page_config(page_title="Cricket Analysis", page_icon=":bar_chart", layout='wide')

## Title and padding 
st.title(":bar_chart: Cricket World Cup Analysis")
st.markdown("<style>div.block-container{padding-top : 1rem;}</style>", unsafe_allow_html=True)

## Adding Style.css 
st.markdown(
    '''
   <style>
    .hover-effect {
        color: white;
        background-color: #155630;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        border-radius: 20px;
        transition-property: background-color, color;
        cursor: pointer;
    }
    .hover-effect:hover {
        background-color: #155655;
        color: #FFF;
        
    }
    hr{
    color:white;
    padding:5px;

    }
    </style>
    ''',
    unsafe_allow_html=True
)

## Reading Data 
data = pd.read_csv('ODI_Match_info.csv')


## Creating Side Bar 
st.sidebar.image('download.jpg')
st.sidebar.header("Get Desire Filters")
## Team 1 Analysis 
team1_unique = data['team1'].unique()
team2_unique = data['team2'].unique()
all_teams = list(set(team1_unique) | set(team2_unique))
Your_Team = st.sidebar.selectbox('Select Your Team', all_teams)
if st.sidebar.button("Analyze"):
     
     st.markdown('<h4 class="hover-effect">Analysis Result</h4>',unsafe_allow_html=True) 
     st.markdown('<br><br>',unsafe_allow_html=True)
     st.write("Matches Played and Won by", Your_Team)
     ## Filtering data for your Team 
     filtered_data = data[(data['team1'] == Your_Team) | (data['team2'] == Your_Team)]
     matches_played = len(filtered_data)
     matches_won = len(filtered_data[filtered_data['winner'] == Your_Team])
     df = pd.DataFrame({
    'Category': [f'Matches Played by {Your_Team}', f'Matches Won By {Your_Team}'],
    'Value': [matches_played, matches_won]})
     color_map = {
    'Matches Played': 'red',
    'Matches Won': 'orange'


    }
     df = df.sort_values('Value', ascending=False)
     fig = px.bar(df, x='Category', y='Value', color='Category', color_discrete_map=color_map)
     fig.update_layout(bargap=0.05)

     fig.update_layout(
    title=f'Comparison of Matches Played and Matches Won By {Your_Team}',
    xaxis_title='Number of Matches Played',
    yaxis_title='Matches won'
    )
     col1,col2 = st.columns([2,2])

     with col1:
          fig.update_layout(width=400, height=500)

          st.plotly_chart(fig)

     with col2:
          st.write("Matches Won By Winning the toss", Your_Team)


          Toss_winner = len(data[data['toss_winner'] == Your_Team])
          Toss_win_match = len(data[(data['toss_winner'] == Your_Team) & (data['winner'] == Your_Team)])
          df = pd.DataFrame({
        'Toss_won': [f"Toss Won by {Your_Team}", "Matches Won when Toss won"],
        'Value': [Toss_winner, Toss_win_match],
         })
       
          color_map = {
        'Toss Won by Your_Team': 'pink',  # Pink color for matches won
        'Matches Won when Toss won': 'lightblue'  # Light blue color for winning the toss
             }  
    
          fig = px.funnel(df, x='Value', y='Toss_won', title="Total wins while winning the toss", color_discrete_map=color_map)
          fig.update_xaxes(categoryorder='total descending')
          fig.update_layout(
           title='Analysis of Toss Outcomes',
           xaxis_title='Category',
           yaxis_title='Value' )
          fig.update_layout(width=550, height=500)


          st.plotly_chart(fig)
     st.markdown("<hr style='border-top: 3px solid #0074D9;'>", unsafe_allow_html=True)

     bowling_first = filtered_data[
    ((filtered_data['toss_winner'] == Your_Team) & (filtered_data['toss_decision'] == 'field')) |
    ((filtered_data['toss_winner'] != Your_Team) & (filtered_data['toss_decision'] == 'bat'))
    ]

     Bowling_First_win = filtered_data[
    ((filtered_data['toss_winner'] == 'Pakistan') & (filtered_data['toss_decision'] == 'field')) |
    ((filtered_data['toss_winner'] != 'Pakistan') & (filtered_data['toss_decision'] == 'bat')) & (filtered_data['winner'] == 'Pakistan')
     ]  
     bowling = pd.DataFrame({
       'key': ['Bowling First', 'Matches Won Bowling first'],
       'value': [len(bowling_first), len(Bowling_First_win)]
         })
     color_map = {
       'Bowling First': 'pink',  # Set the color for 'Bowling First' to pink
      'Matches Won Bowling first': 'lightblue'  # Set the color for 'Matches Won Bowling first' to lightblue
       }
     fig = px.bar(bowling, x='key', y='value', color_discrete_map= color_map)
     fig.update_layout(width=400, height=500)

     fig.update_layout(
    title=f'Matches Won by bowling first by  {Your_Team}',
    xaxis_title='Outcome',
    yaxis_title='Count of Matches'
     )
     col3,col4 = st.columns(2)
     with col3:
          st.plotly_chart(fig)
     with col4:
        batting_first = filtered_data[
                  ((filtered_data['toss_winner'] == Your_Team) & (filtered_data['toss_decision'] == 'bat')) |
              ((filtered_data['toss_winner'] != Your_Team) & (filtered_data['toss_decision'] == 'field'))
       ]
        bating_First_win = filtered_data[
          ((filtered_data['toss_winner'] == 'Pakistan') & (filtered_data['toss_decision'] == 'bat')) |
         ((filtered_data['toss_winner'] != 'Pakistan') & (filtered_data['toss_decision'] == 'field')) & (filtered_data['winner'] == 'Pakistan')
        ]  
        bating = pd.DataFrame({
       'key': ['bating First', 'Matches Won Bating  first'],
       'value': [len(batting_first), len(bating_First_win)]
        })
        fig = px.bar(bating, x='key', y='value', color='key')

        fig.update_layout(
        title=f'Matches Won BY Batting First {Your_Team}',
        xaxis_title='Outcome',
        yaxis_title='Count of Matches'
        )
        fig.update_layout(width=550, height=500)


        st.plotly_chart(fig)
     st.markdown("<hr style='border-top: 3px solid #0074D9;'>", unsafe_allow_html=True)
     
     pakistan_field_first = data[(data['toss_winner'] == Your_Team) & (data['toss_decision'] == 'field')]
     matches_won = pakistan_field_first[pakistan_field_first['winner'] == Your_Team].shape[0]
     matches_lost = pakistan_field_first[pakistan_field_first['winner'] != Your_Team].shape[0]

     fig = px.bar(x=['Matches Won', 'Matches Lost'], y=[matches_won, matches_lost], color=['Matches Won', 'Matches Lost'])
     fig.update_layout(
     title='won the toss choose to bowl first Result',
     xaxis_title='Fielding First',
     yaxis_title='Count'
      )
     st.plotly_chart(fig)
     pakistan_field_first = data[(data['toss_winner'] == Your_Team) & (data['toss_decision'] == 'bat')]
     matches_won = pakistan_field_first[pakistan_field_first['winner'] == Your_Team].shape[0]

     matches_lost = pakistan_field_first[pakistan_field_first['winner'] != Your_Team].shape[0]
     fig = px.bar(x=['Matches Won', 'Matches Lost'], y=[matches_won, matches_lost], color=['Matches Won', 'Matches Lost'])
     fig.update_layout(
     title='Won The Toss Decision of Bating Result',
     xaxis_title='bat First',
     yaxis_title='Count',
     )
     st.plotly_chart(fig)
     pakistan_wins = filtered_data[filtered_data['winner'] == Your_Team]
     season_wins = pakistan_wins['season'].value_counts().reset_index()
     season_wins.columns = ['Season', 'Wins']
     fig = px.bar(season_wins, x='Season', y='Wins', title='Wins in Every Season',color='Wins')
     fig.update_layout(xaxis_title='Season', yaxis_title='Number of Wins')
     st.plotly_chart(fig)
## Now Creating Option for 2nd team 
played_teams = data[(data['team1'] == Your_Team) | (data['team2'] == Your_Team)]
opposite_teams = list(set(played_teams['team1'].unique()) | set(played_teams['team2'].unique()))
opposite_teams.remove(Your_Team)
Opposite_team = st.sidebar.selectbox("Select Opposite Team", opposite_teams)
if st.sidebar.button("Analyze::"):
     filtered_data = data[((data['team1'] == Your_Team) & (data['team2'] == Opposite_team))
                     | ((data['team1'] == Opposite_team) & (data['team2'] == Your_Team))]
     total_matches_played = len(filtered_data)
     st.write(f'Total Matches Played by {Your_Team} and {Opposite_team} are {total_matches_played}')

     first = len(filtered_data[filtered_data['winner']==Your_Team])
     sndteam= len(filtered_data[filtered_data['winner']==Opposite_team])
     dataframe = pd.DataFrame(
          {
               'key':[f'{Your_Team} won',f'{Opposite_team} won'],
               'value':[first,sndteam]
          }
     )

     fig = px.bar(dataframe, x ='key', y='value')
     fig.update_layout(width=400, height=500)
     col5,col6 = st.columns(2)

     with col5:
        st.plotly_chart(fig)
    
    
    # Count how many times Your_Team batted first and lost
     batting_first_losses_your_team = len(filtered_data[
    (filtered_data['toss_winner'] == Your_Team) &
    (filtered_data['toss_decision'] == 'bat') &
    (filtered_data['winner'] != Your_Team)
     ])

# Count how many times Opposite_team batted first and lost
     batting_first_losses_opposite_team = len(filtered_data[
    (filtered_data['toss_winner'] == Opposite_team) &
    (filtered_data['toss_decision'] == 'bat') &
    (filtered_data['winner'] != Opposite_team)
    ])
     with col6:
# Create a bar chart to display the results
      data = pd.DataFrame({
    'Team': [Your_Team, Opposite_team],
    'Batted First and Lost': [batting_first_losses_your_team, batting_first_losses_opposite_team]
      })

     fig = px.bar(data, x='Team', y='Batted First and Lost', color='Team')
     fig.update_layout(width=400, height=500)

     st.plotly_chart(fig)
     batting_first_wins_your_team = len(filtered_data[
    (filtered_data['team1'] == Your_Team) &
    (filtered_data['toss_decision'] == 'bat') &
    (filtered_data['winner'] == Your_Team)
])

# Count how many times Opposite_team batted first and won
     batting_first_wins_opposite_team = len(filtered_data[
    (filtered_data['team1'] == Opposite_team) &
    (filtered_data['toss_decision'] == 'bat') &
    (filtered_data['winner'] == Opposite_team)
])

# Count how many times Your_Team bowled first and won
     bowling_first_wins_your_team = len(filtered_data[
    (filtered_data['team1'] == Your_Team) &
    (filtered_data['toss_decision'] == 'field') &
    (filtered_data['winner'] == Your_Team)
])

# Count how many times Opposite_team bowled first and won
     bowling_first_wins_opposite_team = len(filtered_data[
    (filtered_data['team1'] == Opposite_team) &
    (filtered_data['toss_decision'] == 'field') &
    (filtered_data['winner'] == Opposite_team)
])

# Create a bar chart to display the results
     data = pd.DataFrame({
    'Team': [Your_Team, Opposite_team],
    'Batted First and Won': [batting_first_wins_your_team, batting_first_wins_opposite_team],
    'Bowled First and Won': [bowling_first_wins_your_team, bowling_first_wins_opposite_team]
})

     fig = px.bar(data, x='Team', y=['Batted First and Won', 'Bowled First and Won'], color='Team')
     st.plotly_chart(fig)

## Creating For Venues 
data = pd.read_csv('ODI_Match_info.csv')
filtered = data[((data['team1'] == Your_Team) & (data['team2'] == Opposite_team)) | ((data['team1'] == Opposite_team) & (data['team2'] == Your_Team))]

common_venues = filtered['venue'].unique()

selected_venue = st.sidebar.selectbox("Select Venue", common_venues)

if st.sidebar.button("Analyze:::"):
    filtered_venue = filtered[
        ((filtered['team1'] == Your_Team) & (filtered['team2'] == Opposite_team) & (filtered['venue'] == selected_venue)) |
        ((filtered['team1'] == Opposite_team) & (filtered['team2'] == Your_Team) & (filtered['venue'] == selected_venue))
    ]

    num_matches = len(filtered_venue)
    st.write(f"Matches Played Between {Your_Team} and {Opposite_team} at venue {selected_venue}: {num_matches}")
    win_counts = filtered_venue['winner'].value_counts().reset_index()
    col7, col8 = st.columns(2)
    with col7:
        fig = px.bar(win_counts, x='winner', y='count')
    fig.update_layout(
        title=f'Number of Wins between {Your_Team} and {Opposite_team} at {selected_venue}',
        xaxis_title='Teams',
        yaxis_title='Number of Wins'
    )
    st.plotly_chart(fig)





col1 , col2 = st.columns(2)

with col1:
    st.markdown(
    '<h4 class="hover-effect">Toss Winning By every country</h4>',
    unsafe_allow_html=True
      )    
    toss_winner_counts = data['toss_winner'].value_counts().reset_index()
    toss_winner_counts.columns = ['Country', 'Count']
    fig = px.bar(toss_winner_counts, x='Country', y='Count', color='Country', title='Total Tosses Won by Country')
    fig.update_layout(xaxis_title='Country', yaxis_title='Count')
    st.plotly_chart(fig)





with col2:
    st.markdown('<h4 class="hover-effect">Toss Winning match winning </h4>',unsafe_allow_html=True)  
   
    team_win_counts = data[data['toss_winner'] == data['winner']]['winner'].value_counts().reset_index()
    team_win_counts.columns = ['Team', 'Wins']
    fig = px.bar(team_win_counts, x='Wins', y='Team', color='Team')
    fig.update_xaxes(categoryorder='total ascending')
    st.plotly_chart(fig)



cl1,cl2= st.columns(2)
with cl1:
    with st.expander("Toss Winning data"):
        st.write(toss_winner_counts.head(4).style.background_gradient(cmap="Blues"))
        csv = toss_winner_counts.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name ="Toss_winner.csv", mime="text/csv",help="Click here to download data ")

with cl2:
    with st.expander("Toss Winning data"):
        st.write(team_win_counts.head(4).style.background_gradient(cmap="Blues"))
        csv = team_win_counts.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name ="Toss_winner_match_winner.csv", mime="text/csv",help="Click here to download data ")

st.markdown("<hr style='border-top: 3px solid #0074D9;'>", unsafe_allow_html=True)
  
st.markdown('<h4 class="hover-effect">Toss Loser Match winner </h4>',unsafe_allow_html=True)  
   
team_wins_counts = data[data['toss_winner'] != data['winner']]['winner'].value_counts().reset_index()
team_wins_counts.columns = ['Team', 'Wins']
fig = px.funnel(team_wins_counts, x='Team', y='Wins', color='Team')
fig.update_layout(width=1000, height=700)
fig.update_xaxes(categoryorder='total descending')

fig.update_layout(title='Teams that Lost Toss but Still Won Matches')

st.plotly_chart(fig)
with st.expander("Toss losing but match winning data"):
        st.write(team_wins_counts.head(4).style.background_gradient(cmap="Blues"))
        csv = team_wins_counts.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name ="Toss_loser_match_winner.csv", mime="text/csv",help="Click here to download data ")



cls1,cls2= st.columns(2)
with cls1:
     st.markdown('<h4 class="hover-effect">Winning Perecentage  </h4>',unsafe_allow_html=True)  
     df = data[['team1', 'team2', 'winner']]
     win_counts = df['winner'].value_counts()
     team1_counts = df['team1'].value_counts()
     team2_counts = df['team2'].value_counts()
     total_matches = team1_counts.add(team2_counts, fill_value=0)
     winning_percentage = (win_counts / total_matches).fillna(0) * 100

     winning_percentage_df = pd.DataFrame({'team': winning_percentage.index, 'percentage': winning_percentage.values})
    
     fig = px.pie(winning_percentage_df, values='percentage', names='team', title='Winning Percentage for Each Team')
     st.plotly_chart(fig)
     with st.expander("Winning Perecentage"):
        st.write(winning_percentage_df.style.background_gradient(cmap="Blues"))
        csv = winning_percentage_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name ="Winning peecntage.csv", mime="text/csv",help="Click here to download data ")

with cls2:
    st.markdown('<h4 class="hover-effect">losing  Perecentage  </h4>',unsafe_allow_html=True)  
    df = data[['team1', 'team2', 'winner']]
    win_counts = df['winner'].value_counts()
    team1_counts = df['team1'].value_counts()
    team2_counts = df['team2'].value_counts()
    total_matches = team1_counts.add(team2_counts, fill_value=0)
    Losing_percentage = (total_matches- win_counts / total_matches).fillna(0) * 100

    Losing_percentage_df = pd.DataFrame({'team': winning_percentage.index, 'percentage': Losing_percentage.values})
    
    fig = px.pie(winning_percentage_df, values='percentage', names='team', title='Losing Percentage for Each Team')
    st.plotly_chart(fig)
    with st.expander("Losing Perecentage"):
        st.write(Losing_percentage_df.style.background_gradient(cmap="Blues"))
        csv = winning_percentage_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name ="Losing_peecntage.csv", mime="text/csv",help="Click here to download data ")

st.markdown("<hr style='border-top: 3px solid #0074D9;'>", unsafe_allow_html=True)


st.markdown('<h4 class="hover-effect">Toss Decision by Every Team </h4>',unsafe_allow_html=True)  
toss_decision_count = data.groupby(['toss_winner', 'toss_decision']).size().reset_index(name='Count')
fig = px.bar(toss_decision_count, x='Count', y='toss_decision', color='toss_winner',title='Toss Decisions by Teams')
fig.update_layout(width=950, height=600)
st.plotly_chart(fig)
with st.expander("Toss Decision Count "):
        st.write(toss_decision_count.style.background_gradient(cmap="Blues"))
        csv = toss_decision_count.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name ="toss_decion.csv", mime="text/csv",help="Click here to download data ")




st.markdown("<hr style='border-top: 3px solid #0074D9;'>", unsafe_allow_html=True)



st.markdown('<h4 class="hover-effect">Total wins </h4>',unsafe_allow_html=True)  


temp3 = data['winner'].value_counts().reset_index()
temp3.columns = ['Team', 'Wins']

fig = px.icicle(temp3, path=['Team'], values='Wins')
fig.update_layout(width=500, height=800)

st.plotly_chart(fig)

with st.expander("Totall wins "):
        st.write(temp3.style.background_gradient(cmap="Blues"))
        csv = temp3.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name ="Total wins.csv", mime="text/csv",help="Click here to download data ")
