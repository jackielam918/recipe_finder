import './RecipesGraph.css';

import { useEffect, useRef } from 'react';

import * as d3module from 'd3'
import d3tip from 'd3-tip'
const d3 = {
  ...d3module,
  tip: d3tip
}


function RecipesGraph({ width, height, recipes }) {
    const svgRef = useRef();
    const margin = {top: 0, right: 80, bottom: 0, left: 0};

    useEffect(() => {
        createGraph();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [recipes]);

    const createGraph = () => {

        var svg = d3.select(svgRef.current);
        d3.select(".recipeDetails").remove()
        svg.selectAll("*").remove();
        svg.attr("width", width)
            .attr("height", height);

        if (recipes.length === 0) {
            svg.append("rect")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("class", "recipesEmptyStateContainer")
            
            svg.append("text")
                .text("Search results will appear here!")
                .attr("class", "recipesEmptyStateText")
                .attr("x", width / 2)
                .attr("y", height / 2)

            return;
        }

        var links = [];
        var linksDict = {}
        var maxDegree = 0;
        var minDegree = 1000;
        var maxMissing = 0;

        recipes = recipes.map(recipe => {
            const similarity = recipe["similarity"];
            recipe["difficulty"] = recipe["minutes"] < 30 ? "Easy" : recipe["minutes"] < 90 ? "Medium" : "Hard";
            recipe["numberOfMissing"] = recipe["recipe_difference"].length;
            if (maxDegree < similarity) {
                maxDegree = similarity;
            }

            if (minDegree > similarity) {
                minDegree = similarity;
            }

            if (!linksDict[recipe["recipeid"]]) {
                linksDict[recipe["recipeid"]] = {};
            }

            recipe["similar_recipe_ids"].forEach(similarRecipeId => {
                if (!linksDict[recipe["recipeid"]][similarRecipeId] &&
                    !(linksDict[similarRecipeId] && linksDict[similarRecipeId][recipe["recipeid"]])) {
                        linksDict[recipe["recipeid"]][similarRecipeId] = 1;
                        links.push({
                            "source": recipe["recipeid"],
                            "target": similarRecipeId
                        });
                    }
            });

            if (maxMissing < recipe["numberOfMissing"]) {
                maxMissing = recipe["numberOfMissing"];
            }

            return recipe;
        });

        var nodeSizeScale = d3.scaleLinear()
                                .domain([minDegree, maxDegree])
                                .range([10, 30]);

        var missingScale = d3.scaleLinear()
                                    .domain([0, maxMissing])
                                    .range(["#fed976", "#bd0026"]);
        
        var difficultyColors = {
            "Easy": "#d0d1e6",
            "Medium": "#74a9cf",
            "Hard": "#045a8d",
        }

        //Force-directed Graph
        var g = svg.append("g");

        var tooltip = d3.tip()
                            .attr('class', 'recipeDetails')
                            .direction('s')
                            .html(function(d) { 

                                var html = "";
                                html += "<div class=\"recipeDetailsTitle\">"; 
                                html += "<p class=\"recipeDetailsLabel\">" + d.name + "</p>";
                                html += "<div class='closeButtonContainer' onclick=\"(function () {var toolTip = document.getElementsByClassName('recipeDetails')[0]; toolTip.style['opacity'] = 0; toolTip.style['pointer-events'] = 'none';})();return false;\"><svg xmlns='http://www.w3.org/2000/svg' width='21px' height='21px'><g><line stroke='white' stroke-width='2px' x1='0' y1='0' x2='21' y2='21'></line><line stroke='white' stroke-width='2px' x1='21' y1='0' x2='0' y2='21'></line></g></svg></div>"
                                html += "</div>";
                                
                                html += "<div class=\"recipeDetailsContent\">";
                                html += "<div class=\"recipeDetailsRow\"> <div class=\"recipeDetailsDifSubs\">";
                                html += "<svg width=\"20\" height=\"20\"><circle r=\"10\" fill=\"" + difficultyColors[d.difficulty] + "\" cx=\"10\" cy=\"10\"></circle></svg>"
                                html += "<p>" + d.difficulty + "</p>"
                                html += "<svg width=\"25\" height=\"20\"><circle class=\"recipeNode\" r=\"7.5\" fill=\"white\" stroke=\"" + missingScale(d.numberOfMissing) + "\" cx=\"15\" cy=\"10\"></circle></svg>"
                                html += "<p>" + d.numberOfMissing.toString() + " missing ingredient" + (d.numberOfMissing > 1 ? "s" : "") + "</p>"
                                html += "</div> </div>";

                                html += "<div class=\"recipeDetailsRow\"> <p class=\"recipeDetailsLabel\">Ingredients:</p> </div>";
                                html += "<div class=\"recipeDetailsRow\"> <ul>";
                                const recipe_difference_ids = new Set(d.recipe_difference_ids);
                                d.ingredient_list.forEach((ingredient, index) => {
                                    if (recipe_difference_ids.has(d.ingredient_list_ids[index])){
                                        html += "<li class=\"missingIngredient\">" + ingredient + "</li>";
                                    } else {
                                        html += "<li>" + ingredient + "</li>";
                                    }
                                })
                                html += "</ul> </div>";

                                html += "<div class=\"recipeDetailsRow\"> <p class=\"recipeDetailsLabel\">Instructions:</p> </div>";

                                html += "<div class=\"recipeDetailsRow\"> <ol>";
                                d.stepslist.forEach(instruction => {
                                    html += "<li>" + instruction + "</li>";
                                })
                                html += "</ol> </div>";
                                html += "</div>";

                                return html;
                            });

        g.call(tooltip);

        const tick = () => {
            node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");

            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
        }

        var force = d3.forceSimulation()
            .nodes(recipes)
            .force("link", d3.forceLink(links).id(d => d.recipeid).distance(125))
            .force('center', d3.forceCenter((width - margin.right) / 2, height / 2))
            .force("charge", d3.forceManyBody().strength(-1000))
            .force("x", d3.forceX())
            .force("y", d3.forceY())
            .alphaTarget(1)
            .on("tick", tick);

        var link = g.selectAll(".links")
            .data(links)
            .enter().append("g")
            .append("line")
            .attr("class", "links");

        const dragstarted = (event) => {
            if (!event.active) force.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        const dragged = (event) => {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }
        
        const dragended = (event) => {
            if (!event.active) force.alphaTarget(0);

            event.subject.fixed = true;
            if (event.subject.fixed === true) {
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }
            else {
                event.subject.fx = null;
                event.subject.fy = null;
            }
        }

        var node = g.selectAll(".node")
            .data(force.nodes())
            .enter().append("g")
            .attr("class", "node")
            .on("click", function(event, d) {
                tooltip.show(d, this);
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        node.append("circle")
                .attr("class", "recipeOuterCircle")
                .attr("r", d => (nodeSizeScale(d.similarity) + 3));
        
        node.append("circle")
                .attr("class", "recipeNode")
                .attr("r", d => nodeSizeScale(d.similarity))
                .attr("fill", d => difficultyColors[d.difficulty])
                .attr("stroke", d => missingScale(d.numberOfMissing));
        
        node.append("text")
                .text(d => d.name)
                .attr("class", "recipeName")
                .attr("x", d => (Math.sqrt(Math.pow(nodeSizeScale(d.similarity), 2) / 2) + 3))
                .attr("y", d => -(Math.sqrt(Math.pow(nodeSizeScale(d.similarity), 2) / 2) + 3));
        
        //Graph Legend
        var legend = svg.append("g")
                            .attr("transform", "translate(" + (width - margin.right) + ", 0)");
        
        var legendBackground = legend.append("rect")
                                        .attr("width", margin.right)
                                        .attr("height", 0)
                                        .attr("fill", "white");

        var i = 0, y = 0;
        var difficultyLevels = Object.keys(difficultyColors);
        
        for (i = 0; i < 3; i++) {
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
        
        for (i = 0; i <= maxMissing; i++) {
            y = (i + 3) * 20 + 30;

            legend.append("circle")
                    .attr("class", "legendRecipeNode")
                    .attr("r", 5)
                    .attr("stroke", missingScale(i))
                    .attr("cx", 15)
                    .attr("cy", y)

            legend.append("text")
                    .text(i + " miss.")
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

        //Zoom and Move the Graph
        const zoom_actions = (event) => {
            g.attr("transform", event.transform)
        }

        const zoom_handler = d3.zoom()
                                .on("zoom", zoom_actions);

        zoom_handler(svg); 

    }

    return (
        <svg class="results" ref={svgRef}></svg>
    );
}

export default RecipesGraph;