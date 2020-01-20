using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    public class Item
    {
        public int Level { get; set; }
        public string Team { get; set; }
        public TimeSpan Time { get; set; }
        public int Value { get; set; }
    }

    class Program
    {
        static void Main(string[] args)
        {
            int i = 1;
            double ii = 1.000001;
            var ttt = 1.0 * i;
            if (ii > 1.0*i)
            {

            }
        }

        static void test(IReadOnlyList<Item> items, IDictionary<string, TimeSpan> timeEndGameByTeam)
        {
            var delta = new TimeSpan(0, 0, 5, 0);
            var endOfTheGame = new TimeSpan(0, 7, 0, 0);
            var countPoint = endOfTheGame.Ticks / delta.Ticks + 1;

            var teams = items.Select(x => x.Team).Distinct().ToList();
            var levels = items.Select(x => x.Level).Distinct().ToList();
            levels.Sort();

            var result = new Item[teams.Count, countPoint];
            var currTime = new TimeSpan(0);
            for (var i = 0; i < countPoint; i++)
            {
                for (var j = 0; j < teams.Count; j++)
                {
                    var score = items.Where(x => x.Team.Equals(teams[j])).Where(x => x.Time <= currTime).ToList();
                    var curLvL = score.Max(x => x.Level);
                    var scoreValue = score.Sum(x => x.Value);
                    if (currTime < timeEndGameByTeam[teams[j]])
                    {
                        var diffSpanEndGame = timeEndGameByTeam[teams[j]] - currTime;
                        var fullTenMinutes = (int)Math.Truncate(diffSpanEndGame.TotalMinutes / 10);
                        scoreValue += fullTenMinutes;
                    }
                    result[j, i] = new Item
                    {
                        Level = curLvL,
                        Team = teams[j],
                        Time = currTime,
                        Value = scoreValue
                    };
                }
                currTime += delta;
            }
        }
    }
}
