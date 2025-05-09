import pandas as pd
import matplotlib.pyplot as plt

f1 = pd.read_csv('result.csv')


# def main():



# def task_2(df):
#     df.




def task_1(df):

    with open('top_3.txt', "w", encoding="utf-8") as f:
        f.write("The top 3 players with the highest and lowest scores for each statistic\n\n") 

        stats = df.columns[5:]

        for stat in stats:
            f.write("------------------------------------------\n")
            new_table = df.loc[df[stat] != 'N/a']
            new_table = new_table.sort_values(stat,ascending = False)

            f.write(f"Statistic: {stat}\n\n")
            f.write("The top 3 highest players:\n")
            for _, row in new_table.head(3).iterrows():
                f.write(f"{row['Name']}  {row[stat]}\n")
            f.write('\n')
            # In ra top 3 thấp nhất theo thứ tự tăng dần
            f.write("The top 3 lowest players:\n")
            for _, row in new_table.tail(3).iloc[::-1].iterrows(): \
                f.write(f"{row['Name']}  {row[stat]}\n")





def team_info(nt, df, team_list):
    a = ['Median of', 'Mean of', 'Std of']
    stat_dict = {}  # Khởi tạo dict cho các kết quả
    
    # Tính toán thống kê cho từng đội
    for stat in df.columns[5:]:
        for i in a:
            b = []  # Danh sách lưu kết quả
            for team in team_list:
                s=pd.DataFrame()
                if team == 'All':
                    s = pd.to_numeric(df.loc[df[stat] != 'N/a', stat], errors='raise')
                else:
                    s = pd.to_numeric(df.loc[(df['Team'] == team) & (df[stat] != 'N/a'), stat], errors='raise')
                
                if i == 'Median of':
                    b.append(s.median())
                elif i == 'Mean of':
                    b.append(s.mean())
                else:
                    b.append(s.std())
        
            stat_dict[f'{i} {stat}'] = b    
            
    # Tạo DataFrame từ dictionary và nối vào nt
    stat_df = pd.DataFrame(stat_dict)
    nt = pd.concat([nt, stat_df], axis=1)
    return nt


def all_info(df, nt):
    a = ['Median of', 'Mean of', 'Std of']
    
    # Tính toán thống kê cho tất cả dữ liệu
    b=[]
    for stat in df.columns[5:]:
        for i in a:
            s = pd.to_numeric(df.loc[df[stat] != 'N/a', stat], errors='raise')
            if i == 'Median of':
                b.append(s.median())
            elif i == 'Mean of':
                b.append(s.mean())
            else:
                b.append(s.std())
    
    return b
            
    
def print_to_result2(nt):
    nt= nt.sort_values(by = 'Teams and all').reset_index(drop = True)
    nt.to_csv('result2.csv')




def task_2(df):
    team_list = df['Team'].unique().tolist()
    team_list.append('All')
    nteam = df['Team'].nunique()
    nt = pd.DataFrame()
    nt['Teams and all'] = team_list
    nt = team_info(nt,df,team_list)
    
    print_to_result2(nt)

def task4():
    import pandas as pd
    df = pd.read_csv('result2.csv')

    # Ép kiểu các cột từ cột thứ 2 trở đi thành số (nếu cần)
    with open('top_teams.txt', "w", encoding="utf-8") as f:
        for col in df.columns[2:]:
            f.write(f"Top team for '{col}':\n")
            top_row = df.nlargest(1, col).iloc[0]  # Lấy dòng đầu tiên
            f.write(f"{top_row['Teams and all']}\n\n")
        

    
def all_distribution():
    # Luu tung cau thu
    t1 = pd.read_csv('result.csv')

    for stat in t1.columns[5:]:
        value = t1  .loc[t1[stat] != 'N/a', stat]
        plt.figure(figsize=(8, 5))
        plt.hist(value, bins=20, edgecolor='black')
        plt.xscale('log')  # log scale trục x
        plt.xlabel(stat)
        plt.ylabel('Frequency')
        plt.title(f'Player_{stat}_distribution')
        plt.tight_layout()
        plt.savefig(f'E:/Python Homework 5_5/All_distribution/Player_{stat}_distribution.png', dpi=300)
        plt.close()


def team_distribution():
    t1 = pd.read_csv('result.csv')
    t1 = t1.replace('N/a', pd.NA)

    for col in t1.columns[5:]:
        t1[col] = pd.to_numeric(t1[col], errors='coerce')

    teams = t1['Team'].unique()

    for stat in t1.columns[5:]:
        for team in teams:
            values = t1.loc[t1['Team'] == team, stat].dropna()
            if len(values) == 0:
                continue

            # Tạo thư mục riêng cho từng đội
        
            # Vẽ biểu đồ
            plt.figure(figsize=(8, 5))
            plt.hist(values, bins=20, edgecolor='black')
            plt.xscale('log')
            plt.xlabel(stat)
            plt.ylabel('Frequency')
            plt.title(f'{team} {stat} Distribution')
            plt.tight_layout()

            # Lưu ảnh vào thư mục đội
            plt.savefig(f'E:/Python Homework 5_5/Team_distribution/{team}_{stat}_distribution.png', dpi=300)
            plt.close()


        

def task3():
    all_distribution()
    team_distribution()
        






if __name__ == "__main__":
    # task_1(f1)
    # nt = task_2(f1)
    task3()