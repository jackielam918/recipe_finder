import './RecipesGraph.css';

import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import SearchIcon from '@material-ui/icons/Search';

function RecipesGraph({ width, height, recipes }) {
    const svgRef = useRef();
    const margin = {top: 0, right: 80, bottom: 0, left: 0};

    useEffect(() => {
        createGraph();
    }, [recipes]);

    const createGraph = () => {

        var svg = d3.select(svgRef.current);
        svg.selectAll("*").remove();
        svg.attr("width", width)
            .attr("height", height);

        if (recipes.length == 0) {
            svg.append("rect")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("class", "recipesEmptyStateContainer")
            
            svg.append("text")
                .text("Search results will appear here!")
                .attr("class", "recipesEmptyStateText")
                .attr("x", width / 2)
                .attr("y", height / 2)
            
            svg.append("SearchIcon")

            return;
        }

        var links = [];
        var linksDict = {}
        var maxDegree = 0;
        var minDegree = 1000;
        var maxSubstitutions = 0;

        recipes = recipes.map(recipe => {
            var numberOfSimilarRecipes = 0;
            recipe["numberOfSimilarRecipes"] = numberOfSimilarRecipes = recipe["similarRecipeIds"].length;
            if (maxDegree < numberOfSimilarRecipes) {
                maxDegree = numberOfSimilarRecipes;
            }

            if (minDegree > numberOfSimilarRecipes) {
                minDegree = numberOfSimilarRecipes;
            }

            if (!linksDict[recipe["id"]]) {
                linksDict[recipe["id"]] = {};
            }

            recipe["similarRecipeIds"].forEach(similarRecipeId => {
                if (!linksDict[recipe["id"]][similarRecipeId] &&
                    !(linksDict[similarRecipeId] && linksDict[similarRecipeId][recipe["id"]])) {
                        linksDict[recipe["id"]][similarRecipeId] = 1;
                        links.push({
                            "source": recipe["id"],
                            "target": similarRecipeId
                        });
                    }
            });

            if (maxSubstitutions < recipe["numberOfSubstitutions"]) {
                maxSubstitutions = recipe["numberOfSubstitutions"];
            }

            return recipe;
        });

        var nodeSizeScale = d3.scaleLinear()
                                .domain([minDegree, maxDegree])
                                .range([15, 40]);

        var substitutionScale = d3.scaleLinear()
                                    .domain([0, maxSubstitutions])
                                    .range(["#fed976", "#bd0026"]);
        
        var difficultyColors = {
            "Easy": "#d0d1e6",
            "Medium": "#74a9cf",
            "Hard": "#045a8d",
        }

        var svg = d3.select(svgRef.current)
            .attr("width", width)
            .attr("height", height)
        
        var g = svg.append("g");

        var force = d3.forceSimulation()
            .nodes(recipes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(125))
            .force('center', d3.forceCenter((width - margin.right) / 2, height / 2))
            .force("charge", d3.forceManyBody().strength(-500))
            .force("x", d3.forceX())
            .force("y", d3.forceY())
            .alphaTarget(1)
            .on("tick", tick)
            

        var link = g.selectAll(".links")
            .data(links)
            .enter().append("g")
            .append("line")
            .attr("class", "links");

        var node = g.selectAll(".node")
            .data(force.nodes())
            .enter().append("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        node.append("circle")
                .attr("class", "recipeOuterCircle")
                .attr("r", d => (nodeSizeScale(d.numberOfSimilarRecipes) + 3))
        
        node.append("circle")
                .attr("class", "recipeNode")
                .attr("r", d => nodeSizeScale(d.numberOfSimilarRecipes))
                .attr("fill", d => difficultyColors[d.difficulty])
                .attr("stroke", d => substitutionScale(d.numberOfSubstitutions));
        
        node.append("text")
                .text(d => d.name)
                .attr("class", "recipeName")
                .attr("x", d => (Math.sqrt(Math.pow(nodeSizeScale(d.numberOfSimilarRecipes), 2) / 2) + 3))
                .attr("y", d => -(Math.sqrt(Math.pow(nodeSizeScale(d.numberOfSimilarRecipes), 2) / 2) + 3));

        var legend = svg.append("g")
                            .attr("transform", "translate(" + (width - margin.right) + ", 0)");
        
        var legendBackground = legend.append("rect")
                .attr("width", margin.right)
                .attr("height", 0)
                .attr("fill", "white");

        var y = 0;
        var difficultyLevels = Object.keys(difficultyColors);
        for (var i = 0; i < 3; i++) {
            y = i * 20 + 20;

            legend.append("circle")
                    .attr("r", 7)
                    .attr("fill", difficultyColors[difficultyLevels[i]])
                    .attr("cx", 15)
                    .attr("cy", y);

            legend.append("text")
                    .text(difficultyLevels[i])
                    .attr("class", "legendText")
                    .attr("x", 25)
                    .attr("y", y);
        }
        
        for (var i = 0; i <= maxSubstitutions; i++) {
            y = (i + 3) * 20 + 30;

            legend.append("circle")
                    .attr("class", "legendRecipeNode")
                    .attr("r", 5)
                    .attr("stroke", substitutionScale(i))
                    .attr("cx", 15)
                    .attr("cy", y)

            legend.append("text")
                    .text(i + " subs.")
                    .attr("class", "legendText")
                    .attr("x", 25)
                    .attr("y", y)
        }

        legendBackground.attr("height", y + 20)

        legend.append("line")
                .attr("x1", 0)
                .attr("x2", 0)
                .attr("y1", 14)
                .attr("y2", y + 7)
                .attr("class", "legendLine")
        
        function tick() {
            
            node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");

            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
        
        }
    
        function dragstarted(event) {
            if (!event.active) force.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }
        
        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }
        
        function dragended(event) {
            if (!event.active) force.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        var zoom_handler = d3.zoom()
            .on("zoom", zoom_actions);

        zoom_handler(svg);     

        function zoom_actions(event){
            g.attr("transform", event.transform)
        }
    }

    return (
        <svg class="results" ref={svgRef}></svg>
    );
}

export default RecipesGraph;